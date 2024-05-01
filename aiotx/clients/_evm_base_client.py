import json
import secrets

import aiohttp
from eth_abi import encode
from eth_account import Account
from eth_hash.auto import keccak
from eth_utils import keccak, to_checksum_address, to_hex

from aiotx.types import BlockParam


class AioTxEVMClient:
    def __init__(self, node_url, chain_id):
        self.node_url = node_url
        self.chain_id = chain_id

    def generate_address(self):
        private_key_bytes = secrets.token_hex(32)
        private_key = "0x" + private_key_bytes
        acct = Account.from_key(private_key)
        return private_key, acct.address

    def get_address_from_private_key(self, private_key: str):
        sender_address = Account.from_key(private_key).address
        return to_checksum_address(sender_address)

    async def get_last_block(self):
        payload = json.dumps({"method": "eth_blockNumber", "params": [], "id": 1, "jsonrpc": "2.0"})

        async with aiohttp.ClientSession() as session:
            async with session.post(self.node_url, data=payload) as response:
                result = await response.json()
                print(result)

    async def get_balance(self, address, block_parameter: BlockParam = BlockParam.LATEST):
        payload = json.dumps(
            {"method": "eth_getBalance", "params": [address, block_parameter.value], "id": 1, "jsonrpc": "2.0"}
        )

        async with aiohttp.ClientSession() as session:
            async with session.post(self.node_url, data=payload) as response:
                result = await response.json()
                print(result)

    async def get_transaction(self, hash):
        payload = json.dumps({"method": "eth_getTransactionByHash", "params": [hash], "id": 1, "jsonrpc": "2.0"})

        async with aiohttp.ClientSession() as session:
            async with session.post(self.node_url, data=payload) as response:
                result = await response.json()
                print(result)

    async def get_token_balance(self, address, contract_address, block_parameter: BlockParam = BlockParam.LATEST):
        function_signature = "balanceOf(address)".encode("UTF-8")
        hash_result = keccak(function_signature)
        method_id = hash_result.hex()[:8]

        # Pad the address to 32 bytes (64 characters)
        padded_address = address.lower().replace("0x", "").zfill(64)

        # Construct the data field
        data = f"0x{method_id}{padded_address}"

        payload = json.dumps(
            {
                "method": "eth_call",
                "params": [{"to": contract_address, "data": data}, block_parameter.value],
                "id": 1,
                "jsonrpc": "2.0",
            }
        )

        print("payload", payload)

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.node_url, data=payload, headers={"Content-Type": "application/json"}
            ) as response:
                result = await response.json()
                print(result)

                if "result" in result:
                    balance_hex = result["result"]
                    balance = int(balance_hex, 16)
                    return balance
                else:
                    raise Exception(f"Error: {result}")

    async def get_transaction_count(self, address, block_parameter: BlockParam = BlockParam.LATEST):
        payload = json.dumps(
            {"method": "eth_getTransactionCount", "params": [address, block_parameter.value], "id": 1, "jsonrpc": "2.0"}
        )

        async with aiohttp.ClientSession() as session:
            async with session.post(self.node_url, data=payload) as response:
                result = await response.json()
                print("result", result)
                if "result" in result:
                    count_hex = result["result"]
                    count = int(count_hex, 16)
                    print("count, count", count)
                    return count
                else:
                    raise Exception(f"Error: {result}")

    async def send_transaction(
        self, private_key: str, to_address: str, amount: int, gas_price: int, gas_limit: int = 21000
    ):

        from_address = Account.from_key(private_key).address
        nonce = await self.get_transaction_count(from_address)
        raw_transaction = self.build_raw_transaction(private_key, to_address, nonce, amount, gas_price, gas_limit)

        payload = json.dumps(
            {"method": "eth_sendRawTransaction", "params": [raw_transaction], "id": 1, "jsonrpc": "2.0"}
        )

        async with aiohttp.ClientSession() as session:
            async with session.post(self.node_url, data=payload) as response:
                result = await response.json()
                return result

    def build_raw_transaction(
        self, private_key: str, to_address: str, nonce: int, amount_in_wei: int, gas_price: int, gas_limit: int = 21000
    ):
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
    ):
        # Get the sender's address
        sender_address = Account.from_key(private_key).address

        # Prepare the transfer function call data
        function_signature = "transfer(address,uint256)"
        function_selector = keccak(function_signature.encode("utf-8"))[:4].hex()
        transfer_data = encode(["address", "uint256"], [to_address, amount])
        data = "0x" + function_selector + transfer_data.hex()

        # Build the transaction
        transaction = {
            "nonce": await self.get_transaction_count(sender_address),
            "gasPrice": gas_price,
            "gas": gas_limit,
            "to": token_address,
            "value": 0,
            "data": data,
            "chainId": self.chain_id,
        }

        # Sign the transaction
        signed_transaction = Account.sign_transaction(transaction, private_key)
        raw_tx = to_hex(signed_transaction.rawTransaction)

        # Send the signed transaction
        payload = {"jsonrpc": "2.0", "method": "eth_sendRawTransaction", "params": [raw_tx], "id": 1}
        async with aiohttp.ClientSession() as session:
            async with session.post(self.node_url, json=payload) as response:
                result = await response.json()
                if "error" in result:
                    raise Exception(f"Error: {result['error']}")
                return result["result"]
