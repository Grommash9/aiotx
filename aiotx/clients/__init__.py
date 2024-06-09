import json

import pkg_resources

from ._evm_base_client import AioTxEVMClient
from ._ton_base_client import AioTxTONClient
from ._tron_base_client import AioTxTRONClient
from ._utxo_base_client import AioTxUTXOClient

__all__ = [
    "AioTxTONClient",
    "AioTxBSCClient",
    "AioTxETHClient",
    "AioTxPolygonClient",
    "AioTxBTCClient",
    "AioTxLTCClient",
    "AioTxTRONClient",
]


class AioTxBSCClient(AioTxEVMClient):
    def __init__(self, node_url: str, headers: dict = {}):
        super().__init__(node_url, headers)
        bep20_abi_json = pkg_resources.resource_string("aiotx.utils", "bep20_abi.json")
        self._bep20_abi = json.loads(bep20_abi_json)

    def _get_abi_entries(self):
        return [entry for entry in self._bep20_abi]


class AioTxETHClient(AioTxEVMClient):
    def __init__(self, node_url: str, headers: dict = {}):
        super().__init__(node_url, headers)
        erc20_abi_json = pkg_resources.resource_string("aiotx.utils", "erc20_abi.json")
        self._erc20_abi = json.loads(erc20_abi_json)

    def _get_abi_entries(self):
        return [entry for entry in self._erc20_abi]


class AioTxPolygonClient(AioTxEVMClient):
    def __init__(self, node_url: str, headers: dict = {}):
        super().__init__(node_url, headers)
        erc20_abi_json = pkg_resources.resource_string("aiotx.utils", "erc20_abi.json")
        self._erc20_abi = json.loads(erc20_abi_json)

    def _get_abi_entries(self):
        return [entry for entry in self._erc20_abi]


class AioTxBTCClient(AioTxUTXOClient):
    def __init__(
        self,
        node_url,
        headers: dict = {},
        testnet=False,
        node_username: str = "",
        node_password: str = "",
        db_url="sqlite+aiosqlite:///aiotx_utxo.sqlite",
    ):
        network_name = "testnet" if testnet else "bitcoin"
        super().__init__(
            node_url,
            headers,
            testnet,
            node_username,
            node_password,
            network_name,
            db_url,
        )


class AioTxLTCClient(AioTxUTXOClient):
    def __init__(
        self,
        node_url,
        headers: dict = {},
        testnet=False,
        node_username: str = "",
        node_password: str = "",
        db_url="sqlite+aiosqlite:///aiotx_utxo.sqlite",
    ):
        network_name = "litecoin_testnet" if testnet else "litecoin"
        super().__init__(
            node_url,
            headers,
            testnet,
            node_username,
            node_password,
            network_name,
            db_url,
        )
