import json
import secrets
import threading
import time
import aiohttp
from eth_abi import encode
from eth_account import Account
from eth_typing import HexStr
from eth_utils import keccak, to_checksum_address, to_hex
import asyncio
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
)
from aiotx.types import BlockParam


class AioTxEVMClient:
    def __init__(self, node_url, chain_id):
        self.node_url = node_url
        self.chain_id = chain_id
        self.monitor = EvmMonitor(self)
        self._monitor_thread = None

    def generate_address(self):
        private_key_bytes = secrets.token_hex(32)
        private_key = "0x" + private_key_bytes
        acct = Account.from_key(private_key)
        return private_key, acct.address

    def get_address_from_private_key(self, private_key: str):
        sender_address = Account.from_key(private_key).address
        return to_checksum_address(sender_address)

    async def get_last_block(self):
        payload = {"method": "eth_blockNumber", "params": []}
        result = await self._make_rpc_call(payload)
        last_block = result["result"]
        return int(last_block, 16)

    async def get_balance(self, address, block_parameter: BlockParam = BlockParam.LATEST) -> int:
        payload = {"method": "eth_getBalance", "params": [address, block_parameter.value]}

        result = await self._make_rpc_call(payload)
        balance = result["result"]
        return 0 if balance == "0x" else int(result["result"], 16)

    async def get_transaction(self, hash):
        payload = {"method": "eth_getTransactionByHash", "params": [hash]}
        result = await self._make_rpc_call(payload)
        if result["result"] is None:
            raise TransactionNotFound(f"Transaction {hash} not found!")
        
    async def get_block_by_number(self, block_number: int, transaction_detail_flag: bool = True):
        payload = {"method": "eth_getBlockByNumber", "params": [hex(block_number), transaction_detail_flag]}
        result = await self._make_rpc_call(payload)
        return result

    async def get_token_balance(self, address, contract_address, block_parameter: BlockParam = BlockParam.LATEST) -> int:
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

    async def get_transaction_count(self, address, block_parameter: BlockParam = BlockParam.LATEST) -> int:
        payload = {"method": "eth_getTransactionCount", "params": [address, block_parameter.value]}
        result = await self._make_rpc_call(payload)
        tx_count = result["result"]
        return 0 if tx_count == "0x" else int(tx_count, 16)

    async def send_transaction(
        self, private_key: str, to_address: str, amount: int, gas_price: int, gas_limit: int = 21000
    ) -> str:

        from_address = Account.from_key(private_key).address
        nonce = await self.get_transaction_count(from_address)
        raw_transaction = self.build_raw_transaction(private_key, to_address, nonce, amount, gas_price, gas_limit)

        payload = {"method": "eth_sendRawTransaction", "params": [raw_transaction]}

        result = await self._make_rpc_call(payload)
        return result

    def build_raw_transaction(
        self, private_key: str, to_address: str, nonce: int, amount_in_wei: int, gas_price: int, gas_limit: int = 21000
    ) -> HexStr:
        transaction = {
            "nonce": nonce,
            "gasPrice": gas_price,
            "gas": gas_limit,
            "to": to_address,
            "value": amount_in_wei,
            "data": b"",
            "chainId": self.chain_id,
        }
        signed_transaction = Account.sign_transaction(transaction, private_key)
        raw_tx = to_hex(signed_transaction.rawTransaction)
        return raw_tx

    async def send_token_transaction(
        self,
        private_key: str,
        to_address: str,
        token_address: str,
        amount: int,
        gas_price: int,
        gas_limit: int = 100000,
    ) -> str:
        sender_address = Account.from_key(private_key).address

        function_signature = "transfer(address,uint256)"
        function_selector = keccak(function_signature.encode("utf-8"))[:4].hex()
        transfer_data = encode(["address", "uint256"], [to_address, amount])
        data = "0x" + function_selector + transfer_data.hex()

        transaction = {
            "nonce": await self.get_transaction_count(sender_address),
            "gasPrice": gas_price,
            "gas": gas_limit,
            "to": token_address,
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
                    if "invalid argument" in error_message and "cannot unmarshal hex string without 0x prefix" in error_message or "cannot unmarshal hex string of odd length into" in error_message or "hex string has length" in error_message:
                        raise InvalidArgumentError(error_message)
                    elif "eth_getLogs and eth_newFilter are limited to a 10,000 blocks range" in error_message:
                        raise BlockRangeLimitExceededError(error_message)
                elif error_code == -32603:
                    raise InternalJSONRPCError(error_message)
                else:
                    raise AioTxError(f"Error {error_code}: {error_message}")
                
    def start_monitoring(self, monitoring_start_block: int = None):
        self._monitor_thread = threading.Thread(target=self._start_monitoring_thread, args=(monitoring_start_block,))
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def _start_monitoring_thread(self, monitoring_start_block):
        
        asyncio.run(self.monitor.start(monitoring_start_block))

    def stop_monitoring(self):
        self.monitor.stop()
        if self._monitor_thread:
            self._monitor_thread.join()
                
class EvmMonitor:
    def __init__(self, client: AioTxEVMClient):
        self.client = client
        self.block_handlers = []
        self.transaction_handlers = []
        self.running = False
        self._latest_block = None

    def on_block(self, func):
        self.block_handlers.append(func)
        return func

    def on_transaction(self, func):
        self.transaction_handlers.append(func)
        return func

    async def start(self, monitoring_start_block):
        self.running = True
        self._latest_block = monitoring_start_block
        while self.running:
            try:
                await self.poll_blocks()
                await asyncio.sleep(1)
            except Exception as e:
                print(f"Error during polling: {e}")
                await asyncio.sleep(2)

    def stop(self):
        self.running = False

    async def poll_blocks(self,):
        if self._latest_block is None:
            self._latest_block = await self.client.get_last_block()
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
                if asyncio.iscoroutinefunction(handler):
                    await handler(transaction)
                else:
                    handler(transaction)
