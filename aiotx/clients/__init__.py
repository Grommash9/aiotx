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

    def __init__(
        self,
        node_url,
        testnet=False,
        node_username: str = "",
        node_password: str = "",
        db_url="sqlite+aiosqlite:///aiotx_utxo.sqlite",
    ):
        network_name = "testnet" if testnet else "bitcoin"
        super().__init__(node_url, testnet, node_username, node_password, network_name, db_url)


class AioTxLTCClient(AioTxUTXOClient):

    def __init__(
        self,
        node_url,
        testnet=False,
        node_username: str = "",
        node_password: str = "",
        db_url="sqlite+aiosqlite:///aiotx_utxo.sqlite",
    ):
        network_name = "litecoin_testnet" if testnet else "litecoin"
        super().__init__(node_url, testnet, node_username, node_password, network_name, db_url)
