import asyncio
import binascii
import decimal
import json
import secrets
from typing import Union

import aiohttp
from eth_abi import decode, encode
from eth_account import Account
from eth_utils import (
    currency,
    decode_hex,
    function_signature_to_4byte_selector,
    keccak,
    to_checksum_address,
    to_hex,
)

from aiotx.clients._base_client import AioTxClient, BlockMonitor
from aiotx.exceptions import (
    AioTxError,
    BlockNotFoundError,
    BlockRangeLimitExceededError,
    ExecutionTimeoutError,
    FilterNotFoundError,
    InternalJSONRPCError,
    InvalidArgumentError,
    InvalidRequestError,
    MethodHandlerCrashedError,
    MethodNotFoundError,
    NetworkError,
    NonceTooLowError,
    ReplacementTransactionUnderpriced,
    StackLimitReachedError,
    TraceRequestLimitExceededError,
    TransactionCostExceedsGasLimitError,
    TransactionNotFound,
    VMExecutionError,
    WrongPrivateKey,
)
from aiotx.types import BlockParam


class AioTxEVMClient(AioTxClient):
    def __init__(self, node_url, chain_id):
        super().__init__(node_url)
        self.chain_id = chain_id
        self.monitor = EvmMonitor(self)
        self._monitoring_task = None

    def generate_address(self):
        private_key_bytes = secrets.token_hex(32)
        private_key = "0x" + private_key_bytes
        acct = Account.from_key(private_key)
        return private_key, acct.address

    def get_address_from_private_key(self, private_key: str):
        try:
            from_address = Account.from_key(private_key).address
        except binascii.Error as e:
            raise WrongPrivateKey(e)
        return to_checksum_address(from_address)

    @staticmethod
    def from_wei(number: int, unit: str) -> Union[int, decimal.Decimal]:
        return currency.from_wei(number, unit)

    @staticmethod
    def to_wei(number: Union[int, float, str, decimal.Decimal], unit: str) -> int:
        return currency.to_wei(number, unit)

    def _get_abi_entries(self):
        # Redefine that in you client
        return []

    def decode_transaction_input(self, input_data: str) -> dict:
        if input_data == "0x":
            return {"function_name": None, "parameters": None}
        for abi_entry in self._get_abi_entries():
            function_name = abi_entry.get("name")
            if function_name is None:
                continue
            input_types = [inp["type"] for inp in abi_entry["inputs"]]
            function_signature = f"{function_name}({','.join(input_types)})"
            function_selector = function_signature_to_4byte_selector(function_signature)

            if input_data.startswith("0x" + function_selector.hex()):
                decoded_data = decode(input_types, decode_hex(input_data[10:]))
                decoded_params = {}
                for i, param in enumerate(decoded_data):
                    param_name = abi_entry["inputs"][i]["name"]
                    param_value = param
                    decoded_params[param_name] = param_value

                return {"function_name": function_name, "parameters": decoded_params}

        return {"function_name": None, "parameters": None}

    async def get_last_block_number(self) -> int:
        payload = {"method": "eth_blockNumber", "params": []}
        result = await self._make_rpc_call(payload)
        last_block = result["result"]
        return int(last_block, 16)

    async def get_block_by_number(self, block_number: int, transaction_detail_flag: bool = True):
        payload = {"method": "eth_getBlockByNumber", "params": [hex(block_number), transaction_detail_flag]}
        result = await self._make_rpc_call(payload)
        return result

    async def get_balance(self, address, block_parameter: BlockParam = BlockParam.LATEST) -> int:
        payload = {"method": "eth_getBalance", "params": [address, block_parameter.value]}
        result = await self._make_rpc_call(payload)
        balance = result["result"]
        return 0 if balance == "0x" else int(result["result"], 16)

    async def get_contract_balance(
        self, address, contract_address, block_parameter: BlockParam = BlockParam.LATEST
    ) -> int:
        function_signature = "balanceOf(address)".encode("UTF-8")
        hash_result = keccak(function_signature)
        method_id = hash_result.hex()[:8]
        padded_address = address.lower().replace("0x", "").zfill(64)
        data = f"0x{method_id}{padded_address}"

        payload = {
            "method": "eth_call",
            "params": [{"to": contract_address, "data": data}, block_parameter.value],
        }

        result = await self._make_rpc_call(payload)
        balance = result["result"]
        return 0 if balance == "0x" else int(balance, 16)

    async def get_contract_decimals(self, contract_address) -> int:
        function_signature = "decimals()".encode("UTF-8")
        hash_result = keccak(function_signature)
        method_id = hash_result.hex()[:8]
        payload = {
            "method": "eth_call",
            "params": [{"to": contract_address, "data": f"0x{method_id}"}, "latest"],
        }
        result = await self._make_rpc_call(payload)
        decimals = result["result"]
        return 0 if decimals == "0x" else int(decimals, 16)

    async def get_gas_price(self) -> int:
        payload = {"method": "eth_gasPrice", "params": []}
        result = await self._make_rpc_call(payload)
        price = result["result"]
        return 0 if price == "0x" else int(result["result"], 16)

    async def get_transaction(self, hash) -> dict:
        payload = {"method": "eth_getTransactionByHash", "params": [hash]}
        result = await self._make_rpc_call(payload)
        if result["result"] is None:
            raise TransactionNotFound(f"Transaction {hash} not found!")
        tx_data = result["result"]
        tx_data["aiotx_decoded_input"] = self.decode_transaction_input(tx_data["input"])
        return tx_data

    async def get_transactions_count(self, address, block_parameter: BlockParam = BlockParam.LATEST) -> int:
        payload = {"method": "eth_getTransactionCount", "params": [address, block_parameter.value]}
        result = await self._make_rpc_call(payload)
        tx_count = result["result"]
        return 0 if tx_count == "0x" else int(tx_count, 16)

    async def send(
        self,
        private_key: str,
        to_address: str,
        amount: int,
        nonce: int = None,
        gas_price: int = None,
        gas_limit: int = 21000,
    ) -> str:
        if gas_price is None:
            gas_price = await self.get_gas_price()

        from_address = self.get_address_from_private_key(private_key)
        if nonce is None:
            nonce = await self.get_transactions_count(from_address, BlockParam.PENDING)
        transaction = {
            "nonce": nonce,
            "gasPrice": gas_price,
            "gas": gas_limit,
            "to": to_checksum_address(to_address),
            "value": amount,
            "data": b"",
            "chainId": self.chain_id,
        }
        signed_transaction = Account.sign_transaction(transaction, private_key)
        raw_tx = to_hex(signed_transaction.rawTransaction)
        payload = {"method": "eth_sendRawTransaction", "params": [raw_tx]}
        result = await self._make_rpc_call(payload)
        return result["result"]

    async def send_token(
        self,
        private_key: str,
        to_address: str,
        contract_address: str,
        amount: int,
        nonce: int = None,
        gas_price: int = None,
        gas_limit: int = 100000,
    ) -> str:
        from_address = self.get_address_from_private_key(private_key)
        if nonce is None:
            nonce = await self.get_transactions_count(from_address, BlockParam.PENDING)
        if gas_price is None:
            gas_price = await self.get_gas_price()
        function_signature = "transfer(address,uint256)"
        function_selector = keccak(function_signature.encode("utf-8"))[:4].hex()
        transfer_data = encode(["address", "uint256"], [to_checksum_address(to_address), amount])
        data = "0x" + function_selector + transfer_data.hex()

        transaction = {
            "nonce": nonce,
            "gasPrice": gas_price,
            "gas": gas_limit,
            "to": contract_address,
            "value": 0,
            "data": data,
            "chainId": self.chain_id,
        }

        signed_transaction = Account.sign_transaction(transaction, private_key)
        raw_tx = to_hex(signed_transaction.rawTransaction)

        payload = {"method": "eth_sendRawTransaction", "params": [raw_tx]}
        result = await self._make_rpc_call(payload)
        return result["result"]

    async def _make_rpc_call(self, payload) -> dict:
        payload["jsonrpc"] = "2.0"
        payload["id"] = 1
        async with aiohttp.ClientSession() as session:
            async with session.post(self.node_url, data=json.dumps(payload)) as response:
                result = await response.json()
                if "error" not in result.keys():
                    return result
                error_code = result["error"]["code"]
                error_message = result["error"]["message"]
                if error_code == -32000:
                    if "header not found" in error_message or "could not find block" in error_message:
                        raise BlockNotFoundError(error_message)
                    elif "stack limit reached" in error_message:
                        raise StackLimitReachedError(error_message)
                    elif "method handler crashed" in error_message:
                        raise MethodHandlerCrashedError(error_message)
                    elif "execution timeout" in error_message:
                        raise ExecutionTimeoutError(error_message)
                    elif "nonce too low" in error_message:
                        raise NonceTooLowError(error_message)
                    elif "filter not found" in error_message:
                        raise FilterNotFoundError(error_message)
                    elif "replacement transaction underpriced" in error_message:
                        raise ReplacementTransactionUnderpriced(error_message)
                    else:
                        raise AioTxError(f"Error {error_code}: {error_message}")
                elif error_code == -32009:
                    raise TraceRequestLimitExceededError(error_message)
                elif error_code == -32010:
                    raise TransactionCostExceedsGasLimitError(error_message)
                elif error_code == -32011:
                    raise NetworkError(error_message)
                elif error_code == -32015:
                    raise VMExecutionError(error_message)
                elif error_code == -32601:
                    if "method not found" in error_message:
                        raise MethodNotFoundError(error_message)
                    elif "failed to parse request" in error_message:
                        raise InvalidRequestError(error_message)
                elif error_code == -32602:
                    if (
                        "invalid argument" in error_message
                        and "cannot unmarshal hex string without 0x prefix" in error_message
                        or "cannot unmarshal hex string of odd length into" in error_message
                        or "hex string has length" in error_message
                    ):
                        raise InvalidArgumentError(error_message)
                    elif "eth_getLogs and eth_newFilter are limited to a 10,000 blocks range" in error_message:
                        raise BlockRangeLimitExceededError(error_message)
                elif error_code == -32603:
                    raise InternalJSONRPCError(error_message)
                else:
                    raise AioTxError(f"Error {error_code}: {error_message}")


class EvmMonitor(BlockMonitor):
    def __init__(self, client: AioTxEVMClient):
        self.client = client
        self.block_handlers = []
        self.transaction_handlers = []
        self.running = False
        self._latest_block = None

    async def poll_blocks(
        self,
    ):
        if self._latest_block is None:
            self._latest_block = await self.client.get_last_block_number()
        block = await self.client.get_block_by_number(self._latest_block)
        await self.process_block(block["result"])
        self._latest_block = self._latest_block + 1

    async def process_block(self, block):
        for handler in self.block_handlers:
            if asyncio.iscoroutinefunction(handler):
                await handler(int(block["number"], 16))
            else:
                handler(int(block["number"], 16))

        for transaction in block["transactions"]:
            for handler in self.transaction_handlers:
                transaction["aiotx_decoded_input"] = self.client.decode_transaction_input(transaction["input"])
                if asyncio.iscoroutinefunction(handler):
                    await handler(transaction)
                else:
                    handler(transaction)
