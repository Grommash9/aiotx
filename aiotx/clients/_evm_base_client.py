import binascii
import decimal
import json
import secrets
import sys
from typing import Union

import aiohttp

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
    RpcConnectionError,
    StackLimitReachedError,
    TraceRequestLimitExceededError,
    TransactionCostExceedsGasLimitError,
    TransactionNotFound,
    VMExecutionError,
    WrongPrivateKey,
)
from aiotx.log import logger
from aiotx.types import BlockParam


class AioTxEVMBaseClient(AioTxClient):
    def __init__(self, node_url: str, headers: dict):
        try:
            import eth_abi  # noqa: F401
            import eth_account  # noqa: F401
            import eth_utils  # noqa: F401
        except ImportError:
            logger.error(
                "The required dependencies for (AioTxETHClient, AioTxBSCClient, AioTxTRONClient, AioTxMATICClient) clients are not installed. "
                "Please install the necessary packages and try again."
                "pip install aiotx[evm]"
            )
            sys.exit(-1)

        super().__init__(node_url, headers)
        self.chain_id = None
        self.monitor = EvmMonitor(self)
        self._monitoring_task = None

    def is_hex(self, value):
        try:
            int(value, 16)
            return True
        except ValueError:
            return False

    def _get_abi_entries(self):
        # Redefine that in you client
        return []

    def decode_transaction_input(self, input_data: str) -> dict:
        from eth_abi import decode
        from eth_abi.exceptions import InsufficientDataBytes, NonEmptyPaddingBytes
        from eth_utils import decode_hex, function_signature_to_4byte_selector

        if input_data == "0x":
            return {"function_name": None, "parameters": None}
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

                except (NonEmptyPaddingBytes, InsufficientDataBytes):
                    # If decoding fails, try to handle potential Tron-specific format
                    try:
                        # For Tron, we need to handle the '41' prefix in the address
                        address_start = 10  # Start of address (after function selector)
                        address_end = 74  # End of address (32 bytes after start)
                        value_start = 74  # Start of value

                        address = input_data[address_start:address_end].replace(
                            "0000000000000000000000", ""
                        )
                        if address.startswith("41"):
                            address = "0x" + address[2:]  # Remove '41' and add '0x'
                        else:
                            address = "0x" + address

                        value = int(input_data[value_start:], 16)

                        decoded_data = [address, value]
                    except Exception as e:
                        logger.warning(
                            f"Failed to decode input for method '{function_signature}'. Error: {str(e)}"
                        )
                        return {"function_name": None, "parameters": None}

                decoded_params = {}
                for i, param in enumerate(decoded_data):
                    param_name = abi_entry["inputs"][i]["name"]
                    param_value = param
                    decoded_params[param_name] = param_value

                return {"function_name": function_name, "parameters": decoded_params}

        return {"function_name": None, "parameters": None}

    async def get_last_block_number(self) -> int:
        payload = {"method": "eth_blockNumber", "params": []}
        last_block = await self._make_rpc_call(payload)
        return int(last_block, 16)

    async def get_block_by_number(
        self, block_number: int, transaction_detail_flag: bool = True
    ):
        payload = {
            "method": "eth_getBlockByNumber",
            "params": [hex(block_number), transaction_detail_flag],
        }
        result = await self._make_rpc_call(payload)
        return result

    async def get_balance(
        self, address, block_parameter: BlockParam = BlockParam.LATEST
    ) -> int:
        payload = {
            "method": "eth_getBalance",
            "params": [address, block_parameter.value],
        }
        balance = await self._make_rpc_call(payload)
        return 0 if balance == "0x" else int(balance, 16)

    async def get_contract_balance(
        self, address, contract_address, block_parameter: BlockParam = BlockParam.LATEST
    ) -> int:
        from eth_utils import (
            keccak,
        )

        function_signature = "balanceOf(address)".encode("UTF-8")
        hash_result = keccak(function_signature)
        method_id = hash_result.hex()[:8]
        padded_address = address.lower().replace("0x", "").zfill(64)
        data = f"0x{method_id}{padded_address}"

        payload = {
            "method": "eth_call",
            "params": [{"to": contract_address, "data": data}, block_parameter.value],
        }

        balance = await self._make_rpc_call(payload)
        return 0 if balance == "0x" else int(balance, 16)

    async def get_contract_decimals(self, contract_address) -> int:
        from eth_utils import keccak

        function_signature = "decimals()".encode("UTF-8")
        hash_result = keccak(function_signature)
        method_id = hash_result.hex()[:8]
        payload = {
            "method": "eth_call",
            "params": [{"to": contract_address, "data": f"0x{method_id}"}, "latest"],
        }
        decimals = await self._make_rpc_call(payload)
        return 0 if decimals == "0x" else int(decimals, 16)

    async def get_transaction(self, hash) -> dict:
        payload = {"method": "eth_getTransactionByHash", "params": [hash]}
        tx_data = await self._make_rpc_call(payload)
        if tx_data is None:
            raise TransactionNotFound(f"Transaction {hash} not found!")
        tx_data["aiotx_decoded_input"] = self.decode_transaction_input(tx_data["input"])
        return tx_data

    async def get_chain_id(self) -> int:
        payload = {"method": "eth_chainId", "params": []}
        tx_count = await self._make_rpc_call(payload)
        return 0 if tx_count == "0x" else int(tx_count, 16)


class AioTxEVMClient(AioTxEVMBaseClient):
    def __init__(self, node_url, headers):
        super().__init__(node_url, headers)
        self.chain_id = None
        self.monitor = EvmMonitor(self)
        self._monitoring_task = None

    def generate_address(self):
        from eth_account import Account

        private_key_bytes = secrets.token_hex(32)
        private_key = "0x" + private_key_bytes
        acct = Account.from_key(private_key)
        return private_key, acct.address

    def get_address_from_private_key(self, private_key: str):
        from eth_account import Account
        from eth_utils import (
            to_checksum_address,
        )

        try:
            from_address = Account.from_key(private_key).address
        except binascii.Error as e:
            raise WrongPrivateKey(e)
        return to_checksum_address(from_address)

    def from_wei(
        self, number: Union[int, str], unit: str = "ether"
    ) -> Union[int, decimal.Decimal]:
        from eth_utils import currency

        if isinstance(number, str):
            if self.is_hex(number):
                number = int(number, 16)
        return currency.from_wei(number, unit)

    def to_wei(
        self, number: Union[int, float, str, decimal.Decimal], unit: str = "ether"
    ) -> int:
        from eth_utils import currency

        if isinstance(number, str):
            if self.is_hex(number):
                number = int(number, 16)
        return currency.to_wei(number, unit)

    async def get_gas_price(self) -> int:
        payload = {"method": "eth_gasPrice", "params": []}
        price = await self._make_rpc_call(payload)
        return 0 if price == "0x" else int(price, 16)

    async def get_transactions_count(
        self, address, block_parameter: BlockParam = BlockParam.LATEST
    ) -> int:
        payload = {
            "method": "eth_getTransactionCount",
            "params": [address, block_parameter.value],
        }
        tx_count = await self._make_rpc_call(payload)
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
        from eth_account import Account
        from eth_utils import (
            to_checksum_address,
            to_hex,
        )

        if gas_price is None:
            gas_price = await self.get_gas_price()

        from_address = self.get_address_from_private_key(private_key)
        if nonce is None:
            nonce = await self.get_transactions_count(from_address, BlockParam.PENDING)
        if self.chain_id is None:
            self.chain_id = await self.get_chain_id()
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
        raw_tx = to_hex(signed_transaction.raw_transaction)
        payload = {"method": "eth_sendRawTransaction", "params": [raw_tx]}
        result = await self._make_rpc_call(payload)
        return result

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
        from eth_abi import encode
        from eth_account import Account
        from eth_utils import (
            keccak,
            to_checksum_address,
            to_hex,
        )

        from_address = self.get_address_from_private_key(private_key)
        if nonce is None:
            nonce = await self.get_transactions_count(from_address, BlockParam.PENDING)
        if gas_price is None:
            gas_price = await self.get_gas_price()
        if self.chain_id is None:
            self.chain_id = await self.get_chain_id()
        function_signature = "transfer(address,uint256)"
        function_selector = keccak(function_signature.encode("utf-8"))[:4].hex()
        transfer_data = encode(
            ["address", "uint256"], [to_checksum_address(to_address), amount]
        )
        data = "0x" + function_selector + transfer_data.hex()

        transaction = {
            "nonce": nonce,
            "gasPrice": gas_price,
            "gas": gas_limit,
            "to": to_checksum_address(contract_address),
            "value": 0,
            "data": data,
            "chainId": self.chain_id,
        }

        signed_transaction = Account.sign_transaction(transaction, private_key)
        raw_tx = to_hex(signed_transaction.raw_transaction)

        payload = {"method": "eth_sendRawTransaction", "params": [raw_tx]}
        result = await self._make_rpc_call(payload)
        return result

    async def get_chain_id(self) -> int:
        payload = {"method": "eth_chainId", "params": []}
        tx_count = await self._make_rpc_call(payload)
        return 0 if tx_count == "0x" else int(tx_count, 16)

    async def _make_rpc_call(self, payload) -> dict:
        payload["jsonrpc"] = "2.0"
        payload["id"] = 1
        logger.info(f"rpc call payload: {payload}")
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.node_url, data=json.dumps(payload), headers=self._headers
            ) as response:
                response_text = await response.text()
                logger.info(f"rpc call result: {response_text}")
                if response.status != 200:
                    raise RpcConnectionError(response_text)
                result = await response.json()
                if "error" not in result.keys():
                    return result["result"]
                error_code = result["error"]["code"]
                error_message = result["error"]["message"]
                if error_code == -32000:
                    if (
                        "header not found" in error_message
                        or "could not find block" in error_message
                    ):
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
                        and "cannot unmarshal hex string without 0x prefix"
                        in error_message
                        or "cannot unmarshal hex string of odd length into"
                        in error_message
                        or "hex string has length" in error_message
                    ):
                        raise InvalidArgumentError(error_message)
                    elif (
                        "eth_getLogs and eth_newFilter are limited to a 10,000 blocks range"
                        in error_message
                    ):
                        raise BlockRangeLimitExceededError(error_message)
                elif error_code == -32603:
                    raise InternalJSONRPCError(error_message)
                else:
                    raise RpcConnectionError(f"Error {error_code}: {error_message}")


class EvmMonitor(BlockMonitor):
    def __init__(self, client: AioTxEVMClient):
        self.client = client
        self.block_handlers = []
        self.transaction_handlers = []
        self.block_transactions_handlers = []
        self.running = False
        self._latest_block = None

    async def poll_blocks(self, _: int):
        network_latest_block = await self.client.get_last_block_number()
        target_block = (
            network_latest_block if self._latest_block is None else self._latest_block
        )
        if target_block > network_latest_block:
            return
        cur_block = await self.client.get_block_by_number(target_block)
        await self.process_block(cur_block, network_latest_block)
        self._latest_block = target_block + 1

    async def process_block(self, cur_block, network_latest_block):
        for handler in self.block_handlers:
            if not isinstance(network_latest_block, int):
                network_latest_block = int(network_latest_block, 16)
            await handler(int(cur_block["number"], 16), network_latest_block)

        for transaction in cur_block["transactions"]:
            transaction["aiotx_decoded_input"] = self.client.decode_transaction_input(
                transaction["input"]
            )
            for handler in self.transaction_handlers:
                await handler(transaction)

        for handler in self.block_transactions_handlers:
            await handler(cur_block["transactions"])
