import json

from ._bitcoin_base_client import AioTxUTXOClient
from ._evm_base_client import AioTxEVMClient


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
    pass


class AioTxLTCClient(AioTxUTXOClient):
    pass
