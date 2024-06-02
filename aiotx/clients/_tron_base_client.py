import json
from typing import Optional

import aiohttp
import pkg_resources
from eth_abi import decode
from eth_abi.exceptions import NonEmptyPaddingBytes
from eth_utils import (
    decode_hex,
    function_signature_to_4byte_selector,
)

from aiotx.clients._base_client import AioTxClient, BlockMonitor
from aiotx.exceptions import RpcConnectionError
from aiotx.log import logger


class AioTxTRONClient(AioTxClient):
    def __init__(
        self, node_url, 
    ):
        super().__init__(node_url)
        self.monitor = TronMonitor(self)
        self._monitoring_task = None
        trc20_abi_json = pkg_resources.resource_string('aiotx.utils', 'trc20_abi.json')
        self._trc20_abi = json.loads(trc20_abi_json)

    def _get_abi_entries(self):
        return [entry for entry in self._trc20_abi]
    
    async def get_last_block_number(self) -> int:
        payload = {"method": "eth_blockNumber", "params": {}}
        last_block = await self._make_rpc_call(payload)
        return int(last_block, 16)

    async def get_block_by_number(self, block_number: int, transaction_detail_flag: bool = True):
        payload = {"method": "eth_getBlockByNumber", "params": [hex(block_number), transaction_detail_flag]}
        result = await self._make_rpc_call(payload)
        return result
    
    def decode_transaction_input(self, input_data: str) -> dict:
        if input_data == "0x":
            return {"function_name": None, "parameters": None}
        # TODO tron input don't starts from 0x so for now we will add that
        if not input_data.startswith("0x"):
            input_data = "0x" + input_data
        for abi_entry in self._get_abi_entries():
            function_name = abi_entry.get("name")
            if function_name is None:
                continue
            input_types = [inp["type"] for inp in abi_entry["inputs"]]
            function_signature = f"{function_name}({','.join(input_types)})"
            function_selector = function_signature_to_4byte_selector(function_signature)

            if input_data.startswith("0x" + function_selector.hex()):
                try:
                    decoded_data = decode(input_types, decode_hex(input_data[10:]))
                except NonEmptyPaddingBytes:
                    logger.warning(
                        f"Input does not match the expected format for the method '{function_name}' "
                        f"to decode the transaction with input '{input_data}'. "
                        "It seems to have its own implementation.")
                    return {"function_name": None, "parameters": None}
                decoded_params = {}
                for i, param in enumerate(decoded_data):
                    param_name = abi_entry["inputs"][i]["name"]
                    param_value = param
                    decoded_params[param_name] = param_value

                return {"function_name": function_name, "parameters": decoded_params}

        return {"function_name": None, "parameters": None}

    async def _make_rpc_call(self, payload) -> dict:
        payload["jsonrpc"] = "2.0"
        payload["id"] = 1
        payload_json = json.dumps(payload)
        headers = {"Content-Type": "application/json"}
        async with aiohttp.ClientSession() as session:
            async with session.post(self.node_url, data=payload_json, headers=headers) as response:
                response_text = await response.text()
                if response.status != 200:
                    raise RpcConnectionError(f"Node response status code: {response.status} response test: {response_text}")
                result = await response.json()
                return result["result"]


class TronMonitor(BlockMonitor):
    def __init__(self, client: AioTxTRONClient, last_block: Optional[int] = None):
        self.client = client
        self.block_handlers = []
        self.transaction_handlers = []
        self.running = False
        self._last_block = last_block

    async def poll_blocks(
        self,
    ):
        network_last_block = await self.client.get_last_block_number()
        target_block = network_last_block if self._latest_block is None else self._latest_block
        if target_block > network_last_block:
            return
        block_data = await self.client.get_block_by_number(target_block)
        await self.process_transactions(block_data["transactions"])
        await self.process_block(target_block)
        self._latest_block = target_block + 1

    async def process_block(self, block):
        for handler in self.block_handlers:
            await handler(block)

    async def process_transactions(self, transactions):
        for transaction in transactions:
            transaction["aiotx_decoded_input"] = self.client.decode_transaction_input(transaction["input"])
            for handler in self.transaction_handlers:
                await handler(transaction)

