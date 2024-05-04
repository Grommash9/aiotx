import asyncio
import json
from typing import Union

import aiohttp

from aiotx.clients._base_client import AioTxClient, BlockMonitor
from aiotx.exceptions import (
    AioTxError,
    BlockNotFoundError,
    InternalJSONRPCError,
    InvalidArgumentError,
    InvalidRequestError,
    MethodNotFoundError,
)


class AioTxUTXOClient(AioTxClient):
    def __init__(self, node_url, node_username, node_password, testnet):
        super().__init__(node_url)
        self.monitor = BitcoinMonitor(self)
        self.node_username = node_username
        self.node_password = node_password
        self.testnet = testnet
        # _derivation_path and _wallet_prefix should be implemented for all networks
        # self._derivation_path = ""
        # self._wallet_prefix = ""

    @staticmethod
    def to_satoshi(amount: Union[int, float]) -> int:
        return int(amount * 10**8)

    @staticmethod
    def from_satoshi(amount: int) -> float:
        return amount / 10**8

    # def generate_address(self) -> dict:        
    #     hdkey = HDKey()
    #     private_key = hdkey.subkey_for_path(self._derivation_path).private_hex
    #     public_key = hdkey.subkey_for_path(self._derivation_path).public_hex
    #     hash160 = hdkey.subkey_for_path(self._derivation_path).hash160
    #     address = pubkeyhash_to_addr_bech32(hash160, prefix=self._wallet_prefix, witver=0, separator='1')

    #     return {
    #         "private_key": private_key,
    #         "public_key": public_key,
    #         "address": address
    #     }

    async def get_last_block_number(self) -> int:
        payload = {"method": "getblockcount", "params": []}
        result = await self._make_rpc_call(payload)
        return result["result"]


    async def get_block_by_number(self, block_number: int, verbosity: int = 2):
        payload = {"method": "getblockhash", "params": [block_number]}
        block_hash = await self._make_rpc_call(payload)
        payload = {"method": "getblock", "params": [block_hash["result"], verbosity]}
        result = await self._make_rpc_call(payload)
        return result["result"]
    
    async def _make_rpc_call(self, payload) -> dict:
        payload["jsonrpc"] = "2.0"
        payload["id"] = "curltest"
        async with aiohttp.ClientSession() as session:
            async with session.post(self.node_url, data=json.dumps(payload), auth=aiohttp.BasicAuth(self.node_username, self.node_password)) as response:
                result = await response.json()
                error = result.get("error")

                if error is None:
                    return result
                
                error_code = error.get("code")
                error_message = error.get("message")
                if error_code == -5:
                    raise BlockNotFoundError(error_message)
                elif error_code == -8:
                    raise InvalidArgumentError(error_message)
                elif error_code == -32600:
                    raise InvalidRequestError(error_message)
                elif error_code == -32601:
                    raise MethodNotFoundError(error_message)
                elif error_code == -32603:
                    raise InternalJSONRPCError(error_message)
                else:
                    raise AioTxError(f"Error {error_code}: {error_message}")


class BitcoinMonitor(BlockMonitor):
    def __init__(self, client: AioTxUTXOClient):
        self.client = client
        self.block_handlers = []
        self.transaction_handlers = []
        self.running = False
        self._latest_block = None

    async def poll_blocks(self,):
        if self._latest_block is None:
            self._latest_block = await self.client.get_last_block_number()
        block_data = await self.client.get_block_by_number(self._latest_block)
        await self.process_block(self._latest_block, block_data)
        self._latest_block = self._latest_block + 1

    async def process_block(self, block_number, block_data):
        for handler in self.block_handlers:
            if asyncio.iscoroutinefunction(handler):
                await handler(block_number)
            else:
                handler(block_number)

        for transaction in block_data["tx"]:
            for handler in self.transaction_handlers:
                if asyncio.iscoroutinefunction(handler):
                    await handler(transaction)
                else:
                    handler(transaction)