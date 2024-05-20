import json
import pkg_resources
from ._evm_base_client import AioTxEVMClient
from ._utxo_base_client import AioTxUTXOClient


class AioTxBSCClient(AioTxEVMClient):
    def __init__(self, node_url, chain_id):
        super().__init__(node_url, chain_id)
        bep20_abi_json = pkg_resources.resource_string('aiotx.utils', 'bep20_abi.json')
        self._bep20_abi = json.loads(bep20_abi_json)

    def _get_abi_entries(self):
        return [entry for entry in self._bep20_abi]


class AioTxETHClient(AioTxEVMClient):
    def __init__(self, node_url, chain_id):
        super().__init__(node_url, chain_id)
        erc20_abi_json = pkg_resources.resource_string('aiotx.utils', 'erc20_abi.json')
        self._erc20_abi = json.loads(erc20_abi_json)

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
