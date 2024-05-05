import json

from ._evm_base_client import AioTxEVMClient
from ._utxo_base_client import AioTxUTXOClient
from bitcoinlib.keys import Key, HDKey
from bitcoinlib.transactions import Transaction, Input, Output
from bitcoinlib.encoding import pubkeyhash_to_addr_bech32


class AioTxBSCClient(AioTxEVMClient):
    def __init__(self, node_url, chain_id):
        super().__init__(node_url, chain_id)
        with open("aiotx/utils/bep20_abi.json") as file:
            bep_20_abi = json.loads(file.read())
        self._bep20_abi = bep_20_abi

    def _get_abi_entries(self):
        return [entry for entry in self._bep20_abi]


class AioTxETHClient(AioTxEVMClient):
    def __init__(self, node_url, chain_id):
        super().__init__(node_url, chain_id)
        with open("aiotx/utils/erc20_abi.json") as file:
            erc20_abi = json.loads(file.read())
        self._erc20_abi = erc20_abi

    def _get_abi_entries(self):
        return [entry for entry in self._erc20_abi]


class AioTxBTCClient(AioTxUTXOClient):

    def __init__(self, node_url, node_username: str = "", node_password: str = "", testnet = False):
        super().__init__(node_url, node_username, node_password, testnet)
        self._derivation_path = "m/84'/0'/0'/0/0"
        self._wallet_prefix = 'tb' if self.testnet else 'bc'

    def generate_address(self) -> dict:        
        hdkey = HDKey()
        private_key = hdkey.subkey_for_path(self._derivation_path).private_hex
        hash160 = hdkey.subkey_for_path(self._derivation_path).hash160
        address = pubkeyhash_to_addr_bech32(hash160, prefix=self._wallet_prefix, witver=0, separator='1')
        return private_key, address
    
    def get_address_from_private_key(self, private_key):
        key = Key(private_key)
        public_key = key.public_hex
        hash160 = key.hash160
        address = pubkeyhash_to_addr_bech32(hash160, prefix=self._wallet_prefix, witver=0, separator='1')

        return {
            "private_key": private_key,
            "public_key": public_key,
            "address": address
        }


class AioTxLTCClient(AioTxUTXOClient):
    
    def __init__(self, node_url, node_username: str = "", node_password: str = "", testnet = False):
        super().__init__(node_url, node_username, node_password, testnet)
        self._derivation_path = "m/84'/2'/0'/0/0"
        self._wallet_prefix = 'tltc' if self.testnet else 'ltc'

    def generate_address(self) -> dict:        
        hdkey = HDKey()
        private_key = hdkey.subkey_for_path(self._derivation_path).private_hex
        hash160 = hdkey.subkey_for_path(self._derivation_path).hash160
        address = pubkeyhash_to_addr_bech32(hash160, prefix=self._wallet_prefix, witver=0, separator='1')
        return private_key, address
    
    def get_address_from_private_key(self, private_key):
        key = Key(private_key)
        public_key = key.public_hex
        hash160 = key.hash160
        address = pubkeyhash_to_addr_bech32(hash160, prefix=self._wallet_prefix, witver=0, separator='1')

        return {
            "private_key": private_key,
            "public_key": public_key,
            "address": address
        }
