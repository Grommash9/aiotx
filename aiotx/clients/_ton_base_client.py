import json
import asyncio
import aiohttp
from tonsdk.contract.wallet import Wallets, WalletVersionEnum
from tonsdk.crypto import mnemonic_new
from tonsdk.crypto._mnemonic import mnemonic_is_valid
from tonsdk.utils import bytes_to_b64str, to_nano
from typing import Optional
from aiotx.clients._base_client import AioTxClient, BlockMonitor
from aiotx.exceptions import (
    AioTxError,
    BlockNotFoundError,
    InvalidArgumentError,
    WrongPrivateKey,
)


class AioTxTONClient(AioTxClient):
    def __init__(self, node_url, wallet_version: WalletVersionEnum = WalletVersionEnum.v3r2, workchain: Optional[int] = None):
        super().__init__(node_url)
        # self.monitor = EvmMonitor(self)
        # self._monitoring_task = None
        self.workchain = workchain
        self.wallet_version = wallet_version

    async def generate_address(self) -> tuple[str, str, str]:
        if self.workchain is None:
            await self._get_network_params()
        wallet_mnemonics = mnemonic_new()
        _mnemonics, _, _, wallet = Wallets.from_mnemonics(wallet_mnemonics, self.wallet_version, self.workchain)
        return (
            " ".join(_mnemonics),
            wallet.address.to_string(is_user_friendly=True, is_url_safe=True),
            wallet.address.to_string(False, False, False),
        )

    def _unpack_mnemonic(self, mnemonic_str: str):
        assert isinstance(mnemonic_str, str), "Mnemonic should be represented as string!"
        mnemonic_list = mnemonic_str.split(" ")
        if not mnemonic_is_valid(mnemonic_list):
            raise WrongPrivateKey("mnemonic phrase not valid!")
        return mnemonic_list

    async def get_address_from_mnemonics(self, wallet_mnemonic: str) -> tuple[str, str]:
        if self.workchain is None:
            await self._get_network_params()
        wallet_mnemonic_list = self._unpack_mnemonic(wallet_mnemonic)
        _, _, _, wallet = Wallets.from_mnemonics(wallet_mnemonic_list, self.wallet_version, self.workchain)
        return wallet.address.to_string(is_user_friendly=True, is_url_safe=True), wallet.address.to_string(
            False, False, False
        )

    async def get_last_master_block(self) -> int:
        payload = {"method": "getMasterchainInfo", "params": {}}
        result = await self._make_rpc_call(payload)
        last_block = result["last"]
        return last_block

    async def get_master_block_shards(self, seqno: int) -> list[dict]:
        payload = {"method": "shards", "params": {"seqno": seqno}}
        result = await self._make_rpc_call(payload)
        print("rasdaesult", result)
        return result["shards"]

    async def get_balance(self, address) -> int:
        payload = {"method": "getAddressBalance", "params": {"address": address}}
        balance_info = await self._make_rpc_call(payload)
        return int(balance_info)

    async def get_address_information(self, address):
        payload = {"method": "getAddressInformation", "params": {"address": address}}
        information = await self._make_rpc_call(payload)
        return information

    async def get_wallet_information(self, address):
        payload = {"method": "getWalletInformation", "params": {"address": address}}
        information = await self._make_rpc_call(payload)
        return information
    
    async def get_transaction_count(self, address) -> int:
        address_information = await self.get_wallet_information(address)
        return address_information.get("seqno", 0)

    async def pack_address(self, address) -> str:
        payload = {"method": "packAddress", "params": {"address": address}}
        packed_address = await self._make_rpc_call(payload)
        return packed_address

    async def get_block_transactions(self, shard, seqno, count=40):
        if self.workchain is None:
            await self._get_network_params()
        payload = {
            "method": "getBlockTransactions",
            "params": {"workchain": self.workchain, "shard": shard, "seqno": seqno, "count": count},
        }
        information = await self._make_rpc_call(payload)
        return information["transactions"]

    async def detect_address(self, address):
        payload = {"method": "detectAddress", "params": {"address": address}}
        information = await self._make_rpc_call(payload)
        return information

    async def send(self, mnemonic, to_address, seqno):
        if self.workchain is None:
            await self._get_network_params()
        _, _, _, wallet = Wallets.from_mnemonics(mnemonic, self.wallet_version, self.workchain)
        query = wallet.create_transfer_message(
            to_addr=to_address, amount=to_nano(float(0.01), "ton"), payload="", seqno=seqno
        )
        boc = bytes_to_b64str(query["message"].to_boc(False))
        return await self.send_boc_return_hash(boc)

    async def send_boc_return_hash(self, boc):
        payload = {"method": "sendBocReturnHash", "params": {"boc": boc}}

        information = await self._make_rpc_call(payload)
        return information

    async def _get_network_params(self):
        master_block_data = await self.get_last_master_block()
        workchain = master_block_data["workchain"]
        shard = master_block_data["shard"]
        seqno = master_block_data["seqno"]
        self.workchain = workchain
        return workchain, shard, seqno

    async def get_transactions(
        self, address, limit: int = None, lt: int = None, hash: str = None, to_lt: int = None, archival: bool = None
    ):
        """
        Retrieves transactions for a given TON account.

        Args:
            address (str): Identifier of the target TON account in any form.
            limit (int, optional): Maximum number of transactions in the response.
            lt (int, optional): Logical time of the transaction to start with. Must be sent with `hash`.
            hash (str, optional): Hash of the transaction to start with, in base64 or hex encoding. Must be sent with `lt`.
            to_lt (int, optional): Logical time of the transaction to finish with (to get transactions from `lt` to `to_lt`).
            archival (bool, optional): By default, the `getTransaction` request is processed by any available liteserver.
                If `archival=True`, only liteservers with full history are used.
        """
        params = {"address": address}
        if lt is not None:
            params["lt"] = lt
        if hash is not None:
            params["hash"] = hash
        if to_lt is not None:
            params["to_lt"] = to_lt
        if archival is not None:
            params["archival"] = archival
        if limit is not None:
            params["limit"] = limit

        payload = {"method": "getTransactions", "params": params}
        information = await self._make_rpc_call(payload)
        return information

    async def _make_rpc_call(self, payload) -> dict:
        payload["jsonrpc"] = "2.0"
        payload["id"] = 1
        payload_json = json.dumps(payload)
        headers = {"Content-Type": "application/json"}
        async with aiohttp.ClientSession() as session:
            async with session.post(self.node_url, data=payload_json, headers=headers) as response:
                response_text = await response.text()
                if response.status != 200:
                    if "cannot find block" in response_text:
                        raise BlockNotFoundError(response_text)
                    if "Incorrect address" in response_text:
                        raise InvalidArgumentError(response_text)
                    raise AioTxError(f"Node response status code: {response.status} response test: {response_text}")
                result = await response.json()
                return result["result"]


class TonMonitor(BlockMonitor):
    def __init__(self, client: AioTxTONClient, last_master_block: Optional[int] = None):
        self.client = client
        self.block_handlers = []
        self.transaction_handlers = []
        self.running = False
        self._last_master_block = last_master_block

    async def poll_blocks(
        self,
    ):
        workchain, shard, seqno = await self.client._ge
        target_block = network_latest_block if self._latest_block is None else self._latest_block
        if target_block > network_latest_block:
            return
        block = await self.client.get_block_by_number(target_block)
        await self.process_block(block["result"])
        self._latest_block = target_block + 1

    async def process_block(self, block):
        for handler in self.block_handlers:
            await handler(int(block["number"], 16))

        for transaction in block["transactions"]:
            for handler in self.transaction_handlers:
                await handler(transaction)


# "https://go.getblock.io/3ea060ad138b45b788f72902e3cf9b38"

# ACCESS_TOKEN = "3ea060ad138b45b788f72902e3cf9b38"

# # getting master block
# curl --location --request GET 'https://go.getblock.io/3ea060ad138b45b788f72902e3cf9b38/getMasterchainInfo'

# # {"ok":true,"result":{"@type":"blocks.masterchainInfo","last":{"@type":"ton.blockIdExt","workchain":-1,"shard":"-9223372036854775808","seqno":38016643,"root_hash":"qe2QTVuhQDOYLNPK2yFxl9nGAsrQ4EY6VVSZn89m6dQ=","file_hash":"p8q63ShU6mOoMR7WX4TB4kXlKlefazFQknWFoMJDiTE="},"state_root_hash":"sRL+rhk/qXpzDweLFEC41+XseK7AScl82e93uLRgpOo=","init":{"@type":"ton.blockIdExt","workchain":-1,"shard":"0","seqno":0,"root_hash":"F6OpKZKqvqeFp6CQmFomXNMfMj2EnaUSOXN+Mh+wVWk=","file_hash":"XplPz01CXAps5qeSWUtxcyBfdAo5zVb1N979KLSKD24="},"@extra":"1716355541.08875:0:0.024924086702997283"}}

# # Getting master block shard blocks
# curl --location --request GET 'https://go.getblock.io/3ea060ad138b45b788f72902e3cf9b38/shards?seqno=38016929'

# # Getting shard transactions
# curl --location --request GET 'https://go.getblock.io/3ea060ad138b45b788f72902e3cf9b38/getBlockTransactions?workchain=0&shard=2305843009213693952&seqno=43657559&root_hash=NwhUKuaOJjGeej2DpfKjVTbpL87ED7tlaTafV1eMq2o=&count=5'

# # Get transactions for address (should include block data to get it for that block only? new ones?)
# curl --location --request GET 'https://go.getblock.io/3ea060ad138b45b788f72902e3cf9b38/getTransactions?address=0:272d1e92e231b278f46b89839c6b22fc0bd8e387b35617f298c1d3ae2eb11d5b&limit=2&hash=40ZmLlSKi/WI0xO8TkXpn7RNscnvKSWPQSwt2HE1poQ='


# from tonsdk.contract.wallet import WalletVersionEnum, Wallets
# from tonsdk.utils import bytes_to_b64str
# from tonsdk.crypto import mnemonic_new


# wallet_workchain = 0
# wallet_version = WalletVersionEnum.v3r2
# wallet_mnemonics = mnemonic_new()

# _mnemonics, _pub_k, _priv_k, wallet = Wallets.from_mnemonics(
#     wallet_mnemonics, wallet_version, wallet_workchain)
# query = wallet.create_init_external_message()
# base64_boc = bytes_to_b64str(query["message"].to_boc(False))

# print("""
# Mnemonic: {}

# Raw address: {}

# Bounceable, url safe, user friendly address: {}

# Base64boc to deploy the wallet: {}
# """.format(wallet_mnemonics,
#            wallet.address.to_string(),
#            wallet.address.to_string(True, True, True),
#            base64_boc))


# # # Get transactions for address (should include block data to get it for that block only? new ones?)
# curl --location --request GET 'https://go.getblock.io/3ea060ad138b45b788f72902e3cf9b38/getTransactions?address=0:272d1e92e231b278f46b89839c6b22fc0bd8e387b35617f298c1d3ae2eb11d5b&limit=2&hash=40ZmLlSKi/WI0xO8TkXpn7RNscnvKSWPQSwt2HE1poQ='

# curl --location --request POST 'https://go.getblock.io/3ea060ad138b45b788f72902e3cf9b38/rest/sendBoc' --header 'Content-Type: application/json' --data-raw '{te6cckECAwEAAQ8AAt+IAJ9vK4gUqMCLXKsssfAigLozwwqp2s5GmDp+L8IV9hqSEYCU4fhOUIzrySDjgJo2xfUQUb2iGmUG5UZmecQphuYEjpEV6wKfEX9vX6/SkVaiIQ5Id+QTma2VfiE+eG4L74AlNTRi/////+AAAAAQAQIA3v8AIN0gggFMl7ohggEznLqxn3Gw7UTQ0x/THzHXC//jBOCk8mCDCNcYINMf0x/TH/gjE7vyY+1E0NMf0x/T/9FRMrryoVFEuvKiBPkBVBBV+RDyo/gAkyDXSpbTB9QC+wDo0QGkyMsfyx/L/8ntVABQAAAAACmpoxc9NEcRRhiEkbrH0HlAcR/tey8wfzgh5UEU+wWBpfLpOODwubg=}'

# curl --location --request POST 'https://go.getblock.io/3ea060ad138b45b788f72902e3cf9b38/jsonRPC' --data-raw {"jsonrpc": "2.0", "method": "getConsensusBlock", "id": "getblock.io"}


# curl --location --request POST 'https://go.getblock.io/3ea060ad138b45b788f72902e3cf9b38/jsonRPC' --header 'Content-Type: application/json' --data-raw '{"jsonrpc": "2.0", "method": "sendBoc", "id": "getblock.io", "boc": "asdasd"}'


# curl --location --request POST 'https://go.getblock.io/3ea060ad138b45b788f72902e3cf9b38/rest//sendBocReturnHash?' --header 'Content-Type: application/json' --data-raw {}


# curl --location --request POST 'https://go.getblock.io/3ea060ad138b45b788f72902e3cf9b38/jsonRPC' --header 'Content-Type: application/json' --data-raw '{"jsonrpc": "2.0", "method": "sendBoc", "id": "getblock.io", "params": {"boc": "te6cckECAwEAAQ8AAt+IAJ9vK4gUqMCLXKsssfAigLozwwqp2s5GmDp+L8IV9hqSEYCU4fhOUIzrySDjgJo2xfUQUb2iGmUG5UZmecQphuYEjpEV6wKfEX9vX6/SkVaiIQ5Id+QTma2VfiE+eG4L74AlNTRi/////+AAAAAQAQIA3v8AIN0gggFMl7ohggEznLqxn3Gw7UTQ0x/THzHXC//jBOCk8mCDCNcYINMf0x/TH/gjE7vyY+1E0NMf0x/T/9FRMrryoVFEuvKiBPkBVBBV+RDyo/gAkyDXSpbTB9QC+wDo0QGkyMsfyx/L/8ntVABQAAAAACmpoxc9NEcRRhiEkbrH0HlAcR/tey8wfzgh5UEU+wWBpfLpOODwubg="}}'
