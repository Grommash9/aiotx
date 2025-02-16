import decimal
import json
from decimal import localcontext
from typing import Optional, Union
from aiotx.types import TronContractType, UnDelegateResourceContractParameters, TransferAssetContractParameters, ResourceType
import aiohttp
import pkg_resources
from tronpy import Tron
from tronpy.keys import PrivateKey
from hashlib import sha3_256
from aiotx.clients._base_client import BlockMonitor
from aiotx.clients._base_client import AioTxClient
from aiotx.exceptions import (
    CreateTransactionError,
    InvalidArgumentError,
    RpcConnectionError,
    TransactionNotFound,
)
from aiotx.log import logger
from aiotx.types import BlockParam

units = {
    "sun": 1,
    "trx": 10**6,
}

MIN_SUN = 1
MAX_SUN = 10**18



def function_signature_to_4byte_selector(signature: str) -> bytes:
    return sha3_256(signature.encode()).digest()[:4]


class AioTxTRONClient(AioTxClient):
    def __init__(
        self,
        node_url: str,
        headers: dict = {},
    ):
        super().__init__(node_url, headers)
        self.monitor = TronMonitor(self)
        self._monitoring_task = None
        trc20_abi_json = pkg_resources.resource_string("aiotx.utils", "trc20_abi.json")
        self._trc20_abi = json.loads(trc20_abi_json)

    def _get_abi_entries(self):
        return [entry for entry in self._trc20_abi]

    def generate_address(self):
        client = Tron()
        return client.generate_address()

    def get_address_from_private_key(self, private_key: str):
        client = Tron()
        try:
            priv_key = PrivateKey(bytes.fromhex(private_key))
        except ValueError as e:
            raise ValueError(
                f"An error has been occurred during private key processing: {e}"
            )

        return client.generate_address(priv_key)

    def _hex_to_base58_address(self, hex_address: str) -> str:
        client = Tron()
        return client.to_base58check_address(hex_address)

    async def send(
        self,
        private_key: str,
        to_address: str,
        amount: int,
        memo: str = "",
    ) -> str:
        if not isinstance(memo, str):
            raise TypeError("Memo should be represented as a string!")
        sender_address_data = self.get_address_from_private_key(private_key)
        sender_address = sender_address_data["base58check_address"]
        created_txd = await self._create_transaction(
            sender_address, to_address, amount, memo
        )
        sig = self.sign_msg_hash(private_key, bytes.fromhex(created_txd["txID"]))
        result = await self.broadcast_transaction(
            [sig],
            created_txd["raw_data_hex"],
            created_txd["raw_data"],
            tx_id=created_txd["txID"],
        )
        if result.get("result"):
            return result["txid"]
        raise CreateTransactionError(
            f"Code: {result.get('code')} Message: {result.get('message')}"
        )

    async def send_token(
        self,
        private_key: str,
        to_address: str,
        contract: str,
        amount: int,
        memo: str = "",
    ):
        if not isinstance(memo, str):
            raise TypeError("Memo should be represented as a string!")
        sender_address_data = self.get_address_from_private_key(private_key)
        sender_address = sender_address_data["base58check_address"]
        created_txd = await self._create_trc20_transfer_transaction(
            sender_address, to_address, amount, contract, memo=memo
        )
        tx_id = created_txd["txID"]
        sig = self.sign_msg_hash(private_key, bytes.fromhex(tx_id))
        result = await self.broadcast_transaction(
            [sig], created_txd["raw_data_hex"], created_txd["raw_data"], tx_id
        )
        if result.get("result"):
            return result["txid"]
        raise CreateTransactionError(
            f"Code: {result.get('code')} Message: {result.get('message')}"
        )

    def sign_msg_hash(self, priv_key: str, message_hash: bytes) -> str:
        """Sign a message hash(sha256)."""
        from coincurve import PrivateKey as CoincurvePrivateKey

        private_key_bytes = bytes.fromhex(priv_key)
        signature_bytes = CoincurvePrivateKey(private_key_bytes).sign_recoverable(
            message_hash,
            hasher=None,
        )
        return signature_bytes.hex()

    async def get_transaction_status(self, tx_id: str):
        result = await self._make_api_call(
            {
                "value": tx_id,
            },
            "POST",
            path="/wallet/gettransactionbyid",
        )
        if not result:
            raise TransactionNotFound
        if "Error" in result.keys():
            raise RpcConnectionError(result["Error"])
        return result
    

    def decode_transaction_input(self, transaction_data: dict) -> dict:
        contract = transaction_data['raw_data']['contract'][0]
        contract_type = contract['type']
        parameter_value = contract['parameter']['value']
        if contract_type == TronContractType.UNDELEGATE_RESOURCE.value:
            if not parameter_value.get("resource"):
                parameter_value["resource"] = "BANDWIDTH"
            return {
                "contract_type": TronContractType.UNDELEGATE_RESOURCE.value,
                "parameters": UnDelegateResourceContractParameters(
                    owner_address = self._hex_to_base58_address(parameter_value['owner_address']),
                    receiver_address= self._hex_to_base58_address(parameter_value['receiver_address']),
                    balance= parameter_value['balance'],
                    resource=ResourceType(parameter_value['resource'])).to_dict()
            }
        elif contract_type == TronContractType.TRANSFER_ASSET.value:
            # Convert hex asset_name to string (if needed)
            return {
                "contract_type": contract_type,
                "parameters": {
                    "owner_address": self._hex_to_base58_address(parameter_value['owner_address']),
                    "to_address": self._hex_to_base58_address(parameter_value['to_address']),
                    "asset_name": parameter_value['asset_name'],
                    "amount": parameter_value['amount']
                }
            }
        

    
        elif contract_type == 'DelegateResourceContract':
            if not parameter_value.get("resource"):
                parameter_value["resource"] = "BANDWIDTH"
            return {
            "contract_type": contract_type,
            "parameters": {
                "owner_address": self._hex_to_base58_address(parameter_value['owner_address']),
                "receiver_address": self._hex_to_base58_address(parameter_value['receiver_address']),
                "balance": parameter_value['balance'],
                "resource": parameter_value['resource']
            }
        }
        
        elif contract_type == 'TransferContract':
            # Handle native TRX transfer
            return {
                "contract_type": contract_type,
                "parameters": {
                    "from": self._hex_to_base58_address(parameter_value['owner_address']),
                    "to": self._hex_to_base58_address(parameter_value['to_address']),
                    "amount": parameter_value['amount']
                }
            }
        
        elif contract_type == "AccountCreateContract":
            return {
                "contract_type": contract_type,
                "parameters": {
                    "owner_address": self._hex_to_base58_address(parameter_value['owner_address']),
                    "account_address": self._hex_to_base58_address(parameter_value['account_address']),
                }
            }
        
        elif contract_type == 'TriggerSmartContract':
            input_data = parameter_value['data']
            if not input_data.startswith("0x"):
                input_data = "0x" + input_data
            method_id = input_data[2:10]

            for abi_entry in self._get_abi_entries():
                function_name = abi_entry.get("name")
                if function_name is None:
                    continue

                input_types = [inp["type"] for inp in abi_entry["inputs"]]
                function_signature = f"{function_name}({','.join(input_types)})"
                function_selector = function_signature_to_4byte_selector(function_signature)

            
                if not input_data.startswith("0x" + function_selector.hex()):
                    continue
                    
                if function_name == "transfer":
                    # For TRC20 token transfers, input_data format is:
                    # 0x + 4 bytes function selector + 32 bytes (address) + 32 bytes (amount)
                    # Example input_data:
                    # 0xa9059cbb0000000000000000000000412a68baf67f1c497d9a4a609276a90dcd6ea7744400000000000000000000000000000000000000000000000000000000d693a400
                    
                    # Extract 20-byte address from the padded 32-byte field
                    # Position 34:74 contains the address with padding
                    # The address comes without '41' prefix and needs to be added
                    address_hex = "41" + input_data[34:74].replace("000000000000000000000000", "")

                    # Extract value from the last 32 bytes
                    value = int(input_data[74:], 16)
                    
                    # Convert address to Base58 format
                    tron_address = self._hex_to_base58_address(address_hex)

                    return {
                        "contract_type": contract_type,
                        "parameters": {
                            "function_name": function_name,
                            "method_id": method_id,
                            "from": self._hex_to_base58_address(parameter_value['owner_address']),
                            "to": tron_address,
                            "value": value,
                            "contract_address": self._hex_to_base58_address(parameter_value['contract_address'])
                        }
                    }
                elif function_name == "transferFrom":
                    # Extract addresses and amount from the input data
                    from_address = "41" + input_data[34:74].replace("000000000000000000000000", "")
                    to_address = "41" + input_data[98:138].replace("000000000000000000000000", "")
                    value = int(input_data[138:], 16)

                    return {
                        "contract_type": contract_type,
                        "parameters": {
                            "function_name": function_name,
                            "method_id": method_id,
                            "from": self._hex_to_base58_address(from_address),
                            "to": self._hex_to_base58_address(to_address),
                            "value": value,
                            "contract_address": self._hex_to_base58_address(parameter_value['contract_address']),
                            "owner": self._hex_to_base58_address(parameter_value['owner_address'])
                        }
                    }
            else:
                # We have iterated through all ABI entries and found no match
                # This means the function is not in the ABI and we cannot decode it
                # Return the function name and parameters as None
                return {
                        "contract_type": contract_type,
                        "parameters": {
                            "method_id": method_id,
                        }
                }
        return {"contract_type": contract_type, "parameters": None}
    
    async def get_account_resource(self, address: str):
        # getaccountresource
        result = await self._make_api_call(
            {
                "address": address,
            },
            "POST",
            path="/wallet/getaccountresource"
        )
        if "Error" in result.keys():
            raise RpcConnectionError(result["Error"])
        return result
    
    async def get_block_by_number(
        self, 
        block_number: Union[int, str], 
    ):

        result = await self._make_api_call(
            {
                "num": block_number,
            },
            "POST",
            path="/wallet/getblockbynum",
        )
        if not result:
            raise TransactionNotFound
        if "Error" in result.keys():
            raise RpcConnectionError(result["Error"])
        return result
    
    async def get_latests_block(self):
        result = await self._make_api_call(
            {},
            "POST",
            path="/wallet/getnowblock",
        )
        if not result:
            raise TransactionNotFound
        if "Error" in result.keys():
            raise RpcConnectionError(result["Error"])
        return result

    async def get_transaction_info(self, tx_id: str):
        result = await self._make_api_call(
            {
                "value": tx_id,
            },
            "POST",
            path="/wallet/gettransactioninfobyid",
        )
        if not result:
            raise TransactionNotFound
        if "Error" in result.keys():
            raise RpcConnectionError(result["Error"])
        return result

    async def broadcast_transaction(
        self,
        signature: list[str],
        raw_data_hex: str,
        raw_data: dict,
        tx_id: str,
        visible: bool = True,
    ):
        result = await self._make_api_call(
            {
                "signature": signature,
                "raw_data_hex": raw_data_hex,
                "raw_data": raw_data,
                "visible": visible,
                "txID": tx_id,
            },
            "POST",
            path="/wallet/broadcasttransaction",
        )
        return result

    async def _create_transaction(
        self, from_address, to_address, amount, memo: str = None
    ):
        payload = {
            "owner_address": from_address,
            "to_address": to_address,
            "amount": amount,
            "visible": True,
        }
        if memo is not None:
            payload["extra_data"] = memo.encode().hex()
        transaction = await self._make_api_call(
            payload, "POST", "/wallet/createtransaction"
        )
        if transaction.get("Error") is not None:
            raise CreateTransactionError(transaction.get("Error"))
        return transaction

    async def _create_trc20_transfer_transaction(
        self,
        sender_address: str,
        to_address: str,
        amount: int,
        contract_address: str,
        fee_limit: int = 15000000000,
        call_value: int = 0,
        visible: bool = True,
        memo: str = None,
    ) -> dict:
        from eth_abi import encode

        # Construct the TRC20 token transfer transaction
        hex_eth_like_address = self.base58_to_hex_address(to_address)
        hex_eth_like_address = "0x" + hex_eth_like_address[2:]

        transfer_data = encode(["address", "uint256"], [hex_eth_like_address, amount])
        parameter = transfer_data.hex()

        transaction = {
            "owner_address": sender_address,
            "contract_address": contract_address,
            "function_selector": "transfer(address,uint256)",
            "parameter": parameter,
            "fee_limit": fee_limit,
            "call_value": call_value,
            "visible": visible,
        }
        if memo is not None:
            transaction["extra_data"] = memo.encode().hex()

        # Make the API call to create the transaction
        result = await self._make_api_call(
            transaction, "POST", path="/wallet/triggersmartcontract"
        )
        if result.get("transaction") is None:
            raise CreateTransactionError(
                f"{result['result'].get('code')} {result['result'].get('message')}"
            )
        return result["transaction"]

    def to_sun(
        self, number: Union[int, float, str, decimal.Decimal], unit: str = "trx"
    ) -> int:
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
            raise TypeError(
                "Unsupported type. Must be one of integer, float, or string"
            )

        s_number = str(number)
        unit_value = units[unit]

        if d_number == decimal.Decimal(0):
            return 0

        if d_number < 1 and "." in s_number:
            with localcontext() as ctx:
                multiplier = len(s_number) - s_number.index(".") - 1
                ctx.prec = multiplier
                d_number = decimal.Decimal(value=number, context=ctx) * decimal.Decimal(
                    10**multiplier
                )
                unit_value /= 10**multiplier

        with localcontext() as ctx:
            ctx.prec = 999
            result_value = decimal.Decimal(
                value=d_number, context=ctx
            ) * decimal.Decimal(unit_value)

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

    async def get_balance(
        self, address, block_parameter: BlockParam = BlockParam.LATEST
    ) -> int:
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
        return await super().get_contract_balance(
            address, contract_address, block_parameter
        )

    async def get_contract_decimals(self, address: str):
        client = Tron()
        if client.is_base58check_address(address):
            address = self.base58_to_hex_address(address)
        return await super().get_contract_decimals(address)

    async def _make_api_call(self, payload, method, path) -> dict:
        url = self.node_url + path
        logger.info(f"api call payload: {payload} method: {method} path: {path}")

        headers = {"Content-Type": "application/json"} if method == "POST" else {}
        headers.update(self._headers)

        if method == "POST":
            payload_json = json.dumps(payload)
            response = await self._make_request(
                method, url, data=payload_json, headers=headers
            )
        else:
            response = await self._make_request(method, url, headers=headers)

        return await self._process_api_answer(response)

    async def _process_api_answer(self, response: aiohttp.ClientResponse) -> dict:
        response_text = await response.text()
        logger.info(f"api call result: {response_text} status: {response.status}")
        if response.status != 200:
            raise RpcConnectionError(
                f"Node response status code: {response.status} response test: {response_text}"
            )
        result = await response.json()
        return result

    async def _make_rpc_call(self, payload, path="/jsonrpc") -> dict:
        payload["jsonrpc"] = "2.0"
        payload["id"] = 1
        payload_json = json.dumps(payload)
        logger.info(f"rpc call payload: {payload}")
        headers = {"Content-Type": "application/json"}
        headers.update(self._headers)

        response = await self._make_request(
            "POST", self.node_url + path, data=payload_json, headers=headers
        )

        response_text = await response.text()
        logger.info(f"rpc call result: {response_text}")
        if response.status != 200:
            raise RpcConnectionError(
                f"Node response status code: {response.status} response test: {response_text}"
            )
        result = await response.json()
        if "error" not in result.keys():
            return result["result"]
        error_code = result["error"]["code"]
        error_message = result["error"]["message"]
        if (
            "invalid characters encountered in Hex string" in error_message
            or "invalid hash value" in error_message
            or "invalid address hash value" in error_message
        ):
            raise InvalidArgumentError(error_message)
        else:
            raise RpcConnectionError(f"Error {error_code}: {error_message}")


class TronMonitor(BlockMonitor):
    def __init__(
        self,
        client: AioTxTRONClient,
        last_block: Optional[int] = None,
        max_retries: int = 3,
        retry_delay: float = 1,
    ):
        self.client = client
        self.block_handlers = []
        self.transaction_handlers = []
        self.block_transactions_handlers = []
        self.running = False
        self._last_block = last_block
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    async def poll_blocks(self, _: int):
        block_data = await self._make_request_with_retry(
            self.client.get_latests_block
        )
        network_last_block = block_data["block_header"]["raw_data"]["number"]
        target_block = (
            network_last_block if self._latest_block is None else self._latest_block
        )
        if target_block > network_last_block:
            return
        await self.process_transactions(block_data["transactions"])
        await self.process_block(target_block, network_last_block)
        self._latest_block = target_block + 1

    async def process_block(self, block, network_last_block):
        for handler in self.block_handlers:
            await handler(block, network_last_block)

    async def process_transactions(self, transactions):
        for transaction in transactions:
            transaction["aiotx_decoded_input"] = self.client.decode_transaction_input(
                transaction
            )
            for handler in self.transaction_handlers:
                await handler(transaction)
        for handler in self.block_transactions_handlers:
            await handler(transactions)
