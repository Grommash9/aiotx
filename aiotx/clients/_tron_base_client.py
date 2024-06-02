import json
from typing import Optional

import aiohttp
import pkg_resources
from tronpy import Tron
from tronpy.keys import PrivateKey

from aiotx.clients._base_client import BlockMonitor
from aiotx.clients._evm_base_client import AioTxEVMBaseClient
from aiotx.exceptions import RpcConnectionError
from aiotx.types import BlockParam


class AioTxTRONClient(AioTxEVMBaseClient):
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
    
    def generate_address(self):
        client = Tron()
        return client.generate_address()
    
    def get_address_from_private_key(self, private_key: str):
        client = Tron()
        priv_key = PrivateKey(bytes.fromhex(private_key))
        return client.generate_address(priv_key)
    
    def hex_address_to_base58(self, hex_address: str) -> str:
        # HACK sometimes we have address with 0x prefix? 
        # Should we handle it somehow?
        if hex_address.startswith("0x"):
            hex_address = hex_address[2:]
        client = Tron()
        if not client.is_hex_address(hex_address):
            raise TypeError("Please provide hex address")
        return client.to_base58check_address(hex_address)
    
    def base58_to_hex_address(self, address) -> str:
        client = Tron()
        if not client.is_base58check_address(address):
            raise TypeError("Please provide base58 address")
        return client.to_hex_address(address)

    async def get_balance(self, address, block_parameter: BlockParam = BlockParam.LATEST) -> int:
        client = Tron()
        if client.is_base58check_address(address):
            address = self.base58_to_hex_address(address)
        return await super().get_balance(address, block_parameter)

    async def get_contract_balance(
        self, address, contract_address, block_parameter: BlockParam = BlockParam.LATEST
    ) -> int:
        client = Tron()
        if client.is_base58check_address(address):
            address = self.base58_to_hex_address(address)
        if client.is_base58check_address(contract_address):
            contract_address = self.base58_to_hex_address(contract_address)
        return await super().get_contract_balance(address, contract_address, block_parameter)
    
    async def get_contract_decimals(self, address: str):
        client = Tron()
        if client.is_base58check_address(address):
            address = self.base58_to_hex_address(address)
        return await super().get_contract_decimals(address)
    
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

