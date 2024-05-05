import asyncio
import json
from typing import Union

import aiohttp
import aiosqlite
from bitcoinlib.encoding import pubkeyhash_to_addr_bech32
from bitcoinlib.keys import HDKey, Key
from bitcoinlib.networks import Network
from bitcoinlib.transactions import Transaction

from aiotx.clients._base_client import AioTxClient, BlockMonitor
from aiotx.exceptions import (
    AioTxError,
    BlockNotFoundError,
    InternalJSONRPCError,
    InvalidArgumentError,
    InvalidRequestError,
    MethodNotFoundError,
)


class AioTxUTXOClient(AioTxClient):
    def __init__(self, node_url, node_username, node_password, testnet):
        super().__init__(node_url)
        self.monitor = UTXOMonitor(self)
        self.node_username = node_username
        self.node_password = node_password
        self.testnet = testnet
        self._network = Network("bitcoinlib_test") if testnet else Network("bitcoin")

    @staticmethod
    def to_satoshi(amount: Union[int, float]) -> int:
        return int(amount * 10**8)

    @staticmethod
    def from_satoshi(amount: int) -> float:
        return amount / 10**8     

    def generate_address(self) -> dict:        
        hdkey = HDKey()
        derivation_path = f"m/84'/{self._network.bip44_cointype}'/0'/0/0"
        private_key = hdkey.subkey_for_path(derivation_path).private_hex
        hash160 = hdkey.subkey_for_path(derivation_path).hash160
        address = pubkeyhash_to_addr_bech32(hash160, prefix=self._network.prefix_bech32, witver=0, separator='1')
        return private_key, address
    
    def get_address_from_private_key(self, private_key):
        key = Key(private_key)
        address = pubkeyhash_to_addr_bech32(
            key.hash160, prefix=self._network.prefix_bech32, witver=0, separator='1')

        return {
            "private_key": private_key,
            "public_key": key.public_hex,
            "address": address
        }

    async def get_last_block_number(self) -> int:
        payload = {"method": "getblockcount", "params": []}
        result = await self._make_rpc_call(payload)
        return result["result"]


    async def get_block_by_number(self, block_number: int, verbosity: int = 2):
        payload = {"method": "getblockhash", "params": [block_number]}
        block_hash = await self._make_rpc_call(payload)
        payload = {"method": "getblock", "params": [block_hash["result"], verbosity]}
        result = await self._make_rpc_call(payload)
        return result["result"]
    
    async def send(self, private_key: str, to_address: str, amount: float, fee: float) -> str:
        from_address = self.get_address_from_private_key(private_key)
        # # Получаем неизрасходованные выходы для адреса отправителя
        # unspent_outputs = await self.get_unspent_outputs(from_address)

        # # Выбираем входы и суммируем их значения
        # inputs = []
        # total_value = 0
        # for output in unspent_outputs:
        #     input_data = (output['txid'], output['vout'], output['amount'])
        #     inputs.append(input_data)
        #     total_value += output['amount']
        #     if total_value >= amount + fee:
        #         break
        total_value = self.to_satoshi(1.5)
        inputs = [("737bef3e8161d15e70f4b230d433f40fb3b5bb197a962289047de12ed9900bb4", 0, total_value)]

        outputs = [
            (to_address, amount),
            (from_address["address"], total_value - amount - fee)
        ]
        raw_transaction = await self.create_transaction(inputs, outputs, [private_key])

        txid = await self.send_transaction(raw_transaction)
        return txid

    async def create_transaction(self, inputs: list, outputs: list, private_keys: list) -> str:
        transaction = Transaction(network="litecoin_testnet", witness_type="segwit")

        for input_data in inputs:
            prev_tx_id, prev_out_index, value = input_data
            transaction.add_input(prev_txid=prev_tx_id, output_n=prev_out_index, value=value, witness_type="segwit")

        for output_data in outputs:
            address, value = output_data
            transaction.add_output(value=value, address=address)

        for i, private_key in enumerate(private_keys):
            key = Key(private_key)
            transaction.sign(key, i)
        return transaction.raw_hex()

    async def send_transaction(self, raw_transaction: str) -> str:
        payload = {"method": "sendrawtransaction", "params": [raw_transaction]}
        result = await self._make_rpc_call(payload)
        return result["result"]

    
    async def _make_rpc_call(self, payload) -> dict:
        payload["jsonrpc"] = "2.0"
        payload["id"] = "curltest"
        async with aiohttp.ClientSession() as session:
            async with session.post(self.node_url, data=json.dumps(payload), auth=aiohttp.BasicAuth(self.node_username, self.node_password)) as response:
                result = await response.json()
                error = result.get("error")

                if error is None:
                    return result
                
                error_code = error.get("code")
                error_message = error.get("message")
                if error_code == -5:
                    raise BlockNotFoundError(error_message)
                elif error_code == -8:
                    raise InvalidArgumentError(error_message)
                elif error_code == -32600:
                    raise InvalidRequestError(error_message)
                elif error_code == -32601:
                    raise MethodNotFoundError(error_message)
                elif error_code == -32603:
                    raise InternalJSONRPCError(error_message)
                else:
                    raise AioTxError(f"Error {error_code}: {error_message}")


class UTXOMonitor(BlockMonitor):
    def __init__(self, client: AioTxUTXOClient):
        self.client = client
        self.block_handlers = []
        self.transaction_handlers = []
        self.running = False
        self._latest_block = None

    async def poll_blocks(self,):
        if self._latest_block is None:
            self._latest_block = await self.client.get_last_block_number()
        block_data = await self.client.get_block_by_number(self._latest_block)
        await self.process_block(self._latest_block, block_data)
        self._latest_block = self._latest_block + 1

    async def process_block(self, block_number, block_data):
        for handler in self.block_handlers:
            if asyncio.iscoroutinefunction(handler):
                await handler(block_number)
            else:
                handler(block_number)

        for transaction in block_data["tx"]:
            for handler in self.transaction_handlers:
                if asyncio.iscoroutinefunction(handler):
                    await handler(transaction)
                else:
                    handler(transaction)

    async def init_db(self):
        async with aiosqlite.connect(self.db_name) as conn:
            async with conn.cursor() as c:
                # Создание таблицы для транзакций
                await c.execute('''CREATE TABLE IF NOT EXISTS transactions
                                (hash TEXT PRIMARY KEY, block_number INTEGER,
                                    from_address TEXT, to_address TEXT, value REAL)''')
                
                # Создание таблицы для адресов
                await c.execute('''CREATE TABLE IF NOT EXISTS addresses
                                (address TEXT PRIMARY KEY, block_number INTEGER)''')
            
            await conn.commit()