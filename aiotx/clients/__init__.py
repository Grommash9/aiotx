import json

from ._evm_base_client import AioTxEVMClient
from ._utxo_base_client import AioTxUTXOClient


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


class AioTxLTCClient(AioTxUTXOClient):
    
    def __init__(self, node_url, node_username: str = "", node_password: str = "", testnet = False):
        super().__init__(node_url, node_username, node_password, testnet)
        self._derivation_path = "m/84'/2'/0'/0/0"
        self._wallet_prefix = 'tltc' if self.testnet else 'ltc'
