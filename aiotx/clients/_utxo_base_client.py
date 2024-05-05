import asyncio
import json
from typing import Optional, Union

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
    def __init__(self, node_url, node_username, node_password, testnet, network_name):
        super().__init__(node_url)
        self.node_username = node_username
        self.node_password = node_password
        self.testnet = testnet
        self._network = Network(network_name)
        self.monitor = UTXOMonitor(self, self._network.name)
        asyncio.run(self.monitor._init_db())

    @staticmethod
    def to_satoshi(amount: Union[int, float]) -> int:
        return int(amount * 10**8)

    @staticmethod
    def from_satoshi(amount: int) -> float:
        return amount / 10**8     

    async def generate_address(self) -> dict:
        hdkey = HDKey()
        derivation_path = f"m/84'/{self._network.bip44_cointype}'/0'/0/0"
        private_key = hdkey.subkey_for_path(derivation_path).private_hex
        hash160 = hdkey.subkey_for_path(derivation_path).hash160
        address = pubkeyhash_to_addr_bech32(hash160, prefix=self._network.prefix_bech32, witver=0, separator='1')
        last_block_number = await self.get_last_block_number()
        await self.import_address(address, last_block_number)
        return private_key, address
    
    async def import_address(self, address: str, block_number: int):
        await self.monitor._add_new_address(address, block_number)
    
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
        from_wallet = self.get_address_from_private_key(private_key)
        from_address = from_wallet["address"]
        # # Получаем неизрасходованные выходы для адреса отправителя
        utxo_list = await self.monitor._get_utxo_data(from_address)

        # Выбираем входы и суммируем их значения
        inputs = []
        total_value = 0
        for utxo in utxo_list:
            input_data = (utxo[0], utxo[1], utxo[2])
            inputs.append(input_data)
            total_value += utxo[2]
            if total_value >= amount + fee:
                break
        # total_value = self.to_satoshi(1.5)
        # inputs = [("737bef3e8161d15e70f4b230d433f40fb3b5bb197a962289047de12ed9900bb4", 0, total_value)]

        outputs = [
            (to_address, amount),
            (from_address, total_value - amount - fee)
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
    def __init__(self, client: AioTxUTXOClient, currency_name, db_name: str = "aiotx_utxo.sqlite"):
        self.client = client
        self.block_handlers = []
        self.transaction_handlers = []
        self.running = False
        self._db_name = db_name
        self._last_block_table_name = f"{currency_name}_last_block"
        self._addresses_table_name = f"{currency_name}_addresses"
        self._utxo_table_name = f"{currency_name}_utxo"

    async def poll_blocks(self):
        latest_block = await self._get_last_block()
        block_data = await self.client.get_block_by_number(latest_block)
        await self.process_block(latest_block, block_data)
        await self._update_last_block(latest_block + 1)

    async def process_block(self, block_number, block_data):
        await self._update_last_block(block_number)
        for handler in self.block_handlers:
            await handler(block_number)

        addresses = await self._get_addresses()
        for transaction in block_data["tx"]:

            for input_utxo in transaction["vin"]:
                txid = input_utxo.get("txid")
                vout = input_utxo.get("vout")
                if txid is None or vout is None:
                    continue
                await self._process_input_utxo(txid, vout)


            for output in transaction["vout"]:
                outputs_scriptPubKey = output.get("scriptPubKey")
                if outputs_scriptPubKey is None:
                    continue

                output_address_list = outputs_scriptPubKey.get("addresses")
                if output_address_list is None:
                    continue

                to_address = output_address_list[0]
                if to_address not in addresses:
                    continue

                value = self.client.to_satoshi(output["value"])
                output_n = output["n"]
                await self._add_new_utxo(to_address, transaction["txid"], value, output_n)


            for handler in self.transaction_handlers:
                await handler(transaction)


    

    async def _init_db(self):
        async with aiosqlite.connect(self._db_name) as conn:
            async with conn.cursor() as c:
                # Создание таблицы для последнего блока
                await c.execute(f'''CREATE TABLE IF NOT EXISTS {self._last_block_table_name}
                                    (block_number INTEGER PRIMARY KEY)''')

                # Создание таблицы для адресов
                await c.execute(f'''CREATE TABLE IF NOT EXISTS {self._addresses_table_name}
                                    (address TEXT PRIMARY KEY, block_number INTEGER)''')

                # Создание таблицы для UTXO
                await c.execute(f'''CREATE TABLE IF NOT EXISTS {self._utxo_table_name}
                                    (address TEXT,
                                    tx_id TEXT,
                                    amount_satoshi INTEGER,
                                    output_n INTEGER,
                                    PRIMARY KEY (tx_id, output_n))''')

            await conn.commit()

            async with conn.cursor() as c:
                await c.execute(f'''SELECT block_number FROM {self._last_block_table_name}''')
                result = await c.fetchone()

            if result is None:
                # Если последний номер блока отсутствует, получаем его и сохраняем в таблицу
                last_block_number = await self.client.get_last_block_number()
                async with conn.cursor() as c:
                    await c.execute(f'''INSERT INTO {self._last_block_table_name}
                                        (block_number) VALUES (?)''', (last_block_number,))
                await conn.commit()

    async def _run_query(self, query, params=None):
        async with aiosqlite.connect(self._db_name) as conn:
            async with conn.cursor() as c:
                try:
                    if params:
                        await c.execute(query, params)
                    else:
                        await c.execute(query)
                    await conn.commit()
                except aiosqlite.OperationalError as e:
                    if "database is locked" in str(e):
                        # Повторная попытка выполнения запроса при возникновении ошибки блокировки
                        await asyncio.sleep(1)
                        return await self._run_query(query, params)
                    else:
                        raise e

    async def _add_new_address(self, address: str, block_number: int):
        query = f'''INSERT OR REPLACE INTO {self._addresses_table_name}
                    (address, block_number) VALUES (?, ?)'''
        await self._run_query(query, (address, block_number))
        last_known_block = await self._get_last_block()
        if last_known_block > block_number:
            await self._update_last_block(block_number)

    async def _add_new_utxo(self, address: str, tx_id: str, amount: int, output_n: int) -> None:
        query = f'''INSERT OR IGNORE INTO {self._utxo_table_name}
                    (address, tx_id, amount_satoshi, output_n) VALUES (?, ?, ?, ?)'''
        await self._run_query(query, (address, tx_id, amount, output_n))

    async def _update_last_block(self, block_number: int) -> None:
        query = f'''UPDATE {self._last_block_table_name} SET block_number = ?'''
        await self._run_query(query, (block_number,))
    
    async def _process_input_utxo(self, txid: str, vout: int):
        utxo = await self._get_utxo(txid, vout)
        if utxo:
            await self._delete_utxo(txid, vout)

    async def _get_utxo_data(self, address: str):
        query = f'''SELECT utxo.tx_id, utxo.output_n, utxo.amount_satoshi
                    FROM {self._utxo_table_name} utxo
                    WHERE utxo.address = ?'''
        async with aiosqlite.connect(self._db_name) as conn:
            async with conn.cursor() as c:
                await c.execute(query, (address,))
                return await c.fetchall()
            
    async def _get_utxo(self, tx_id: str, output_n: int) -> Optional[tuple]:
        query = f'''SELECT utxo.tx_id, utxo.output_n
                    FROM {self._utxo_table_name} utxo
                    WHERE utxo.tx_id = ? and output_n = ?'''
        async with aiosqlite.connect(self._db_name) as conn:
            async with conn.cursor() as c:
                await c.execute(query, (tx_id, output_n))
                return await c.fetchone()
            
    async def _delete_utxo(self, tx_id: str, output_n: int):
        query = f'''DELETE FROM {self._utxo_table_name}
                    WHERE tx_id = ? AND output_n = ?'''
        await self._run_query(query, (tx_id, output_n))


    async def _get_last_block(self) -> Optional[int]:
        query = f'''SELECT block_number FROM {self._last_block_table_name}'''
        async with aiosqlite.connect(self._db_name) as conn:
            async with conn.cursor() as c:
                await c.execute(query)
                result = await c.fetchone()
                return result[0] if result else None

    async def _get_addresses(self) -> Optional[int]:
        query = f'''SELECT address FROM {self._addresses_table_name}'''
        async with aiosqlite.connect(self._db_name) as conn:
            async with conn.cursor() as c:
                await c.execute(query)
                result = await c.fetchall()
                return {address[0] for address in result}