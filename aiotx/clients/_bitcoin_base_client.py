from aiotx.clients._base_client import AioTxClient


class AioTxUTXOClient(AioTxClient):

    def __init__(self, node_url):
        self.node_url = node_url

    def generate_address(self):
        pass

    def get_balance(self, address):
        pass
