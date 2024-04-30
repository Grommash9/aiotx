import secrets
from eth_utils import keccak, encode_hex, to_checksum_address
from eth_keys import keys

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

    def get_balance(self, address):
        pass
