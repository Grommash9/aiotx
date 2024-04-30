from _bitcoin_base_client import AioTxUTXOClient
from _evm_base_client import AioTxEVMClient


class AioTxBSCClient(AioTxEVMClient):
    pass


class AioTxETHClient(AioTxEVMClient):
    pass


class AioTxBTCClient(AioTxUTXOClient):
    pass


class AioTxLTCClient(AioTxUTXOClient):
    pass
