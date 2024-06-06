import decimal
import json
from decimal import localcontext
from typing import Optional, Union
from aiohttp import ClientResponse
import aiohttp
from tronpy.contract import Contract, ContractMethod, ShieldedTRC20
import pkg_resources
from tronpy.tron import TransactionBuilder, Transaction
from tronpy import Tron
from tronpy.keys import PrivateKey
from tronpy.providers.http import HTTPProvider
from aiotx.clients._base_client import BlockMonitor
from aiotx.clients._evm_base_client import AioTxEVMBaseClient
from aiotx.exceptions import InvalidArgumentError, RpcConnectionError
from aiotx.types import BlockParam
import hashlib
from tronpy.keys import keccak256

units = {
    "sun": 1,
    "trx": 10 ** 6,
}

MIN_SUN = 1
MAX_SUN = 10 ** 18



class CustomTransactionBuilder(TransactionBuilder):

    def __init__(self, builder: TransactionBuilder, client: "Tron", method: ContractMethod = None):
        super().__init__(builder._raw_data, client, method)
        self._builder = builder

    def build(self, options=None, ref_block_bytes=None, ref_block_hash=None, **kwargs) -> "Transaction":
        """Build the transaction with custom ref_block_bytes and ref_block_hash."""
        if ref_block_bytes is not None and ref_block_hash is not None:
            # Use the provided ref_block_bytes and ref_block_hash
            self._raw_data["ref_block_bytes"] = ref_block_bytes
            self._raw_data["ref_block_hash"] = ref_block_hash
        else:
            # Retrieve the latest solid block ID
            ref_block_id = self._client.get_latest_solid_block_id()
            # last 2 byte of block number part
            self._raw_data["ref_block_bytes"] = ref_block_id[12:16]
            # last half part of block hash
            self._raw_data["ref_block_hash"] = ref_block_id[16:32]

        if self._method:
            return Transaction(self._raw_data, client=self._client, method=self._method)
        return Transaction(self._raw_data, client=self._client)

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
            hex_address = hex_address.replace("0x", "41")
        client = Tron()
        if not client.is_hex_address(hex_address):
            raise TypeError("Please provide hex address")
        return client.to_base58check_address(hex_address)
    
    def base58_to_hex_address(self, address) -> str:
        client = Tron()
        if not client.is_base58check_address(address):
            raise TypeError("Please provide base58 address")
        return client.to_hex_address(address)
    
    async def send(
        self,
        private_key: str,
        to_address: str,
        amount: int
    ) -> str:
        priv_key = PrivateKey(bytes.fromhex(private_key))
        sender_address_data = self.get_address_from_private_key(private_key)
        sender_address = sender_address_data["base58check_address"]
        created_txd = await self.create_transaction(sender_address, to_address, amount)
        sig = priv_key.sign_msg_hash(bytes.fromhex(created_txd["txID"]))
        result = await self.broadcast_transaction([sig.hex()], created_txd["raw_data_hex"], created_txd["raw_data"], tx_id=created_txd["txID"])
        return result["txid"]
    
    async def broadcast_transaction(self, signature: list[str], raw_data_hex: str, raw_data: dict, tx_id: str, visible: bool = True):
        result = await self._make_api_call({"signature": signature, "raw_data_hex": raw_data_hex, "raw_data": raw_data, "visible": visible, "txID": tx_id}, "POST", path="/wallet/broadcasttransaction")
        return result

    async def get_latest_solidity_block(self):
        transaction = await self._make_api_call({}, "GET", "/walletsolidity/getnowblock")

        return transaction
    
    async def create_transaction(self, from_address, to_address, amount):
        payload = {
        "owner_address": from_address,
        "to_address": to_address,
        "amount": amount,
        "visible": True
        }
        transaction = await self._make_api_call(payload, "POST", "/wallet/createtransaction")
        return transaction
    

    
    async def get_account(self, address):
        payload = {"address": address, "visible": True}
        account_data = await self._make_api_call(payload, "POST", "/wallet/getaccount")

        return account_data
    
    def to_sun(self, number: Union[int, float, str, decimal.Decimal], unit: str = "trx") -> int:
        """
        Takes a number of a unit and converts it to Sun (the smallest unit of TRX).
        """
        unit = unit.lower()
        if unit not in units:
            raise ValueError(f"Unknown unit. Must be one of {'/'.join(units.keys())}")

        if isinstance(number, int) or isinstance(number, str):
            d_number = decimal.Decimal(value=number)
        elif isinstance(number, float):
            d_number = decimal.Decimal(value=str(number))
        elif isinstance(number, decimal.Decimal):
            d_number = number
        else:
            raise TypeError("Unsupported type. Must be one of integer, float, or string")

        s_number = str(number)
        unit_value = units[unit]

        if d_number == decimal.Decimal(0):
            return 0

        if d_number < 1 and "." in s_number:
            with localcontext() as ctx:
                multiplier = len(s_number) - s_number.index(".") - 1
                ctx.prec = multiplier
                d_number = decimal.Decimal(value=number, context=ctx) * 10 ** multiplier
                unit_value /= 10 ** multiplier

        with localcontext() as ctx:
            ctx.prec = 999
            result_value = decimal.Decimal(value=d_number, context=ctx) * unit_value

        if result_value < MIN_SUN or result_value > MAX_SUN:
            raise ValueError("Resulting Sun value must be between 1 and 10^18")

        return int(result_value)

    def from_sun(self, number: Union[int, str], unit: str = "trx") -> decimal.Decimal:
        """
        Converts a value in Sun (the smallest unit of TRX) to the specified unit.
        """
        if isinstance(number, str):
            if number.startswith("0x"):
                number = int(number, 16)
            else:
                number = int(number)

        unit = unit.lower()
        if unit not in units:
            raise ValueError(f"Unknown unit. Must be one of {'/'.join(units.keys())}")

        unit_value = units[unit]
        result_value = decimal.Decimal(number) / unit_value

        return result_value

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

    
    async def _make_api_call(self, payload, method, path) -> dict:
        url = self.node_url + path
        async with aiohttp.ClientSession() as session:
            if method == "POST":
                headers = {"Content-Type": "application/json"}
                payload_json = json.dumps(payload)
                async with session.post(url, data=payload_json, headers=headers) as response:
                    return await self._process_api_answer(response)
            async with session.get(url) as response:
                return await self._process_api_answer(response)
                
            
    async def _process_api_answer(self, response: ClientResponse) -> dict:
        response_text = await response.text()
        print("response_text", response_text)
        if response.status != 200:
            raise RpcConnectionError(f"Node response status code: {response.status} response test: {response_text}")
        result = await response.json()
        return result

    async def _make_rpc_call(self, payload, path="/jsonrpc") -> dict:
        payload["jsonrpc"] = "2.0"
        payload["id"] = 1
        payload_json = json.dumps(payload)
        headers = {"Content-Type": "application/json"}
        async with aiohttp.ClientSession() as session:
            async with session.post(self.node_url + path, data=payload_json, headers=headers) as response:
                response_text = await response.text()
                print("response_text", response_text)
                if response.status != 200:
                    raise RpcConnectionError(f"Node response status code: {response.status} response test: {response_text}")
                result = await response.json()
                if "error" not in result.keys():
                    return result["result"]
                error_code = result["error"]["code"]
                error_message = result["error"]["message"]
                if (
                        "invalid characters encountered in Hex string" in error_message or
                        "invalid hash value" in error_message or
                        "invalid address hash value" in error_message
                    ):
                        raise InvalidArgumentError(error_message)
                else:
                    raise RpcConnectionError(f"Error {error_code}: {error_message}")


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

