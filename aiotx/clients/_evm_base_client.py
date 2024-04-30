import secrets
from eth_utils import keccak, encode_hex, to_checksum_address
from eth_keys import keys
import aiohttp
import json
from aiotx.types import BlockParam
from eth_hash.auto import keccak



class AioTxEVMClient:
    def __init__(self, node_url):
        self.node_url = node_url

    def generate_address(self):
        private_key_bytes = secrets.token_bytes(32)
        private_key = keys.PrivateKey(private_key_bytes)
        public_key_bytes = private_key.public_key.to_bytes()
        keccak_digest = keccak(public_key_bytes)[12:]
        address = encode_hex(keccak_digest[-20:])
        private_key_hex = private_key.to_hex()
        return private_key_hex, to_checksum_address(address)

    
    def get_address_from_private_key(self, private_key_hex: str):
        private_key = keys.PrivateKey(bytes.fromhex(private_key_hex[2:]))
        public_key_bytes = private_key.public_key.to_bytes()
        keccak_digest = keccak(public_key_bytes)[12:]
        address = encode_hex(keccak_digest[-20:])
        return to_checksum_address(address)


    async def get_last_block(self):
        payload = json.dumps({
            "method": "eth_blockNumber",
            "params": [],
            "id": 1,
            "jsonrpc": "2.0"
        })

        async with aiohttp.ClientSession() as session:
            async with session.post(self.node_url, data=payload) as response:
                result = await response.json()
                print(result)

    async def get_balance(self, address, block_parameter: BlockParam = BlockParam.LATEST):
        payload = json.dumps({
            "method": "eth_getBalance",
            "params": [address, block_parameter.value],
            "id": 1,
            "jsonrpc": "2.0"
        })

        async with aiohttp.ClientSession() as session:
            async with session.post(self.node_url, data=payload) as response:
                result = await response.json()
                print(result)
    
    async def get_transaction(self, hash):
        payload = json.dumps({
            "method": "eth_getTransactionByHash",
            "params": [hash],
            "id": 1,
            "jsonrpc": "2.0"
        })

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

        payload = json.dumps({
            "method": "eth_call",
            "params": [{"to": contract_address, "data": data}, block_parameter.value],
            "id": 1,
            "jsonrpc": "2.0"
        })

        print("payload", payload)

        async with aiohttp.ClientSession() as session:
            async with session.post(self.node_url, data=payload, headers={"Content-Type": "application/json"}) as response:
                result = await response.json()
                print(result)

                if "result" in result:
                    balance_hex = result["result"]
                    balance = int(balance_hex, 16)
                    return balance
                else:
                    raise Exception(f"Error: {result}")
