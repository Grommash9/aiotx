import json
from typing import Optional

import aiohttp
from tonsdk.contract.wallet import Wallets, WalletVersionEnum
from tonsdk.crypto import mnemonic_new
from tonsdk.crypto._mnemonic import mnemonic_is_valid
from tonsdk.utils import bytes_to_b64str, to_nano

from aiotx.clients._base_client import AioTxClient, BlockMonitor
from aiotx.exceptions import (
    AioTxError,
    BlockNotFoundError,
    InvalidArgumentError,
    WrongPrivateKey,
)


class AioTxTONClient(AioTxClient):
    def __init__(
        self, node_url, wallet_version: WalletVersionEnum = WalletVersionEnum.v3r2, workchain: Optional[int] = None
    ):
        super().__init__(node_url)
        self.monitor = TonMonitor(self)
        self._monitoring_task = None
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

    async def get_block_transactions(self, workchain, shard, seqno, count=40):
        # Here we don't have workchain by default, because in mainnet
        # for example master block workchain is -1 and shard is 0
        # So we should use workchain here
        payload = {
            "method": "getBlockTransactions",
            "params": {"workchain": workchain, "shard": shard, "seqno": seqno, "count": count},
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
        workchain, shard, seqno = await self.client._get_network_params()
        if self.client.workchain is None:
            self.client.workchain = workchain
        target_block = seqno if self._latest_block is None else self._latest_block
        if target_block > seqno:
            return
        shards = await self.client.get_master_block_shards(target_block)
        for shard in shards:
            shard_transactions = await self.client.get_block_transactions(
                shard["workchain"], shard["shard"], shard["seqno"], 1000
            )
            await self.process_shard_transactions(shard_transactions)
        await self.process_master_block(target_block)
        self._latest_block = target_block + 1

    async def process_master_block(self, block):
        for handler in self.block_handlers:
            await handler(block)

    async def process_shard_transactions(self, shard_transactions):
        for transaction in shard_transactions:
            for handler in self.transaction_handlers:
                await handler(transaction)

