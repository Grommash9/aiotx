import asyncio
import hashlib
import json
from typing import Optional, Union

import aiohttp
import bech32
import ecdsa
from base58 import b58encode
from bech32 import bech32_encode, convertbits
from bitcoinlib.keys import Key
from bitcoinlib.transactions import Transaction
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

from aiotx.clients._base_client import AioTxClient, BlockMonitor
from aiotx.exceptions import (
    AioTxError,
    BlockNotFoundError,
    InternalJSONRPCError,
    InvalidArgumentError,
    InvalidRequestError,
    MethodNotFoundError,
)

Base = declarative_base()

def create_address_model(currency_name):
    class Address(Base):
        __tablename__ = f"{currency_name}_addresses"
        __table_args__ = {'extend_existing': True}

        address = Column(String(255), primary_key=True)
        block_number = Column(Integer)

    return Address

def create_utxo_model(currency_name):
    class UTXO(Base):
        __tablename__ = f"{currency_name}_utxo"
        __table_args__ = {'extend_existing': True}

        tx_id = Column(String(255), primary_key=True)
        output_n = Column(Integer, primary_key=True)
        address = Column(String(255))
        amount_satoshi = Column(Integer)

    return UTXO

def create_last_block_model(currency_name):
    class LastBlock(Base):
        __tablename__ = f"{currency_name}_last_block"
        __table_args__ = {'extend_existing': True}

        block_number = Column(Integer, primary_key=True)

    return LastBlock


class AioTxUTXOClient(AioTxClient):
    def __init__(self, node_url, testnet, hrp, db_url):
        super().__init__(node_url)
        self.testnet = testnet
        self._hrp = hrp
        self.monitor = UTXOMonitor(self, db_url)
        asyncio.run(self.monitor._init_db())

    @staticmethod
    def to_satoshi(amount: Union[int, float]) -> int:
        return int(amount * 10**8)

    @staticmethod
    def from_satoshi(amount: int) -> float:
        return amount / 10**8     

    async def generate_address(self):
        private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        public_key = private_key.get_verifying_key()
        public_key_bytes = public_key.to_string(encoding='compressed')
        witness_version = 0
        witness_program = hashlib.new('ripemd160', hashlib.sha256(public_key_bytes).digest()).digest()
        data = [witness_version] + convertbits(witness_program, 8, 5)
        bech32_address = bech32_encode(self._hrp, data)
        private_key_hex = private_key.to_string().hex()
        last_block_number = await self.get_last_block_number()
        await self.import_address(bech32_address, last_block_number)
        return private_key_hex, bech32_address

    def to_wif(private_key_hex):
        private_key_bytes = bytes.fromhex(private_key_hex)
        extended_key = b'\x80' + private_key_bytes
        hashed_key = hashlib.sha256(hashlib.sha256(extended_key).digest()).digest()
        checksum = hashed_key[:4]
        payload = extended_key + checksum
        wif_key = b58encode(payload).decode('utf-8')
        return wif_key   

    def get_address_from_private_key(self, private_key):
        private_key_bytes = bytes.fromhex(private_key)
        signing_key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
        verifying_key = signing_key.get_verifying_key()
        public_key_bytes = verifying_key.to_string(encoding='compressed')
        witness_version = 0
        witness_program = hashlib.new('ripemd160', hashlib.sha256(public_key_bytes).digest()).digest()
        data = [witness_version] + bech32.convertbits(witness_program, 8, 5)
        bech32_address = bech32.bech32_encode(self._hrp, data)
        return {
        "private_key": private_key,
        "public_key": public_key_bytes.hex(),
        "address": bech32_address
        }
    
    async def import_address(self, address: str, block_number: int = None):
        await self.monitor._add_new_address(address, block_number)


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
    
    async def get_balance(self, address: str) -> int:
        utxo_data = await self.monitor._get_utxo_data(address)
        if len(utxo_data) == 0:
            return 0
        return sum(utxo.amount_satoshi for utxo in utxo_data)
    
    async def _build_and_send_transaction(self, private_key: str, destinations: dict[str, int], fee: float) -> str:
        from_wallet = self.get_address_from_private_key(private_key)
        from_address = from_wallet["address"]
        utxo_list = await self.monitor._get_utxo_data(from_address)

        inputs = []
        outputs = []
        total_amount = sum(destinations.values())
        total_value = 0
        for utxo in utxo_list:
            input_data = (
                utxo.tx_id,
                utxo.output_n,
                utxo.amount_satoshi
            )
            inputs.append(input_data)
            total_value += utxo.amount_satoshi
            if total_value >= total_amount + fee:
                break
            
        leftover = total_value - total_amount - fee

        if leftover > 0:
            outputs.append((from_address, leftover))

        for address, amount in destinations.items():
            outputs.append((address, amount))
        
        signed_tx = await self.create_and_sign_transaction(inputs, outputs, [private_key] * len(inputs))
        txid = await self.send_transaction(signed_tx)
        return txid


    async def send(self, private_key: str, to_address: str, amount: int, fee: int) -> str:
        return await self._build_and_send_transaction(private_key, {to_address: amount}, fee)
    
    async def send_bulk(self, private_key: str, destinations: dict[str, int], fee: int) -> str:
        return await self._build_and_send_transaction(private_key, destinations, fee)

    async def create_and_sign_transaction(self, inputs: list, outputs: list, private_keys: list) -> str:
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

    # def sign_transaction(self, raw_transaction, private_key):
    #     private_key_bytes = bytes.fromhex(private_key)
    #     signing_key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)

    #     transaction_bytes = bytes.fromhex(raw_transaction)
    #     hash_tx = hashlib.sha256(hashlib.sha256(transaction_bytes).digest()).digest()
    #     signature = signing_key.sign_digest(hash_tx, sigencode=ecdsa.util.sigencode_der)
    #     encoded_signature = signature.hex()
    #     sighash_all = '01'
    #     final_signature = encoded_signature + sighash_all

    #     public_key = signing_key.get_verifying_key().to_string("compressed").hex()

    #     # Construct the witness data
    #     witness = [final_signature, public_key]

    #     # Extract the script_pub_key from the raw transaction
    #     script_pub_key = raw_transaction[-44:]

    #     # Construct the signed transaction
    #     signed_transaction = raw_transaction[:-44] + '00' + script_pub_key

    #     # Append the witness data separately
    #     witness_data = []
    #     for item in witness:
    #         witness_data.append('{:02x}'.format(len(item) // 2))
    #         witness_data.append(item)

    #     # Calculate the number of witness items
    #     num_witness_items = len(witness_data) // 2

    #     # Construct the witness data string
    #     witness_data_str = '{:02x}'.format(num_witness_items) + ''.join(witness_data)

    #     # Calculate the length of the witness data string
    #     witness_data_len = '{:02x}'.format(len(witness_data_str) // 2)

    #     # Append the witness data to the signed transaction
    #     signed_transaction += '0100' + witness_data_len + witness_data_str

    #     return signed_transaction
    

    async def send_transaction(self, raw_transaction: str) -> str:
        payload = {"method": "sendrawtransaction", "params": [raw_transaction]}
        result = await self._make_rpc_call(payload)
        return result["result"]

    
    async def _make_rpc_call(self, payload) -> dict:
        payload["jsonrpc"] = "2.0"
        payload["id"] = "curltest"
        async with aiohttp.ClientSession() as session:
            async with session.post(self.node_url, data=json.dumps(payload), auth=aiohttp.BasicAuth("litecoinrpc", "7aON+t6CMysoGC7U7dOwCipjpzE=")) as response:
                # print("response", response)
                result = await response.json()
                # print("result", result)
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
    def __init__(self, client: AioTxUTXOClient, db_url):
        self.client = client
        self.block_handlers = []
        self.transaction_handlers = []
        self.running = False
        self._db_url = db_url
        self._engine = create_async_engine(db_url, poolclass=NullPool)
        self._session = sessionmaker(self._engine, class_=AsyncSession, expire_on_commit=False)
        self.Address = create_address_model(self.client._hrp)
        self.UTXO = create_utxo_model(self.client._hrp)
        self.LastBlock = create_last_block_model(self.client._hrp)

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
                output_address = outputs_scriptPubKey.get("address")

                if output_address is None and output_address_list is None:
                    continue

                if output_address_list is not None:
                    to_address = output_address_list[0]
                else:
                    to_address = output_address
                
                if to_address not in addresses:
                    continue

                value = self.client.to_satoshi(output["value"])
                output_n = output["n"]
                await self._add_new_utxo(to_address, transaction["txid"], value, output_n)


            for handler in self.transaction_handlers:
                await handler(transaction)


    async def _init_db(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            last_known_block = await self.client.get_last_block_number()
            await self._init_last_block(last_known_block)


    async def _add_new_address(self, address: str, block_number: int = None):
        last_known_block = await self.client.get_last_block_number()
        if block_number is None:
            block_number = last_known_block

        async with self._session() as session:
            async with session.begin():
                session.add(self.Address(address=address, block_number=block_number))
                await session.commit()

        last_known_block = await self._get_last_block()
        if last_known_block > block_number:
            await self._update_last_block(block_number)

    async def _add_new_utxo(self, address: str, tx_id: str, amount: int, output_n: int) -> None:
        async with self._session() as session:
            async with session.begin():
                session.add(self.UTXO(address=address, tx_id=tx_id, amount_satoshi=amount, output_n=output_n))
                await session.commit()

    
    async def _update_last_block(self, block_number: int) -> None:
        async with self._session() as session:
            async with session.begin():
                data = await session.execute(select(self.LastBlock))
                last_block = data.scalar()
                last_block.block_number = block_number
                await session.commit()
    
    async def _init_last_block(self, block_number: int) -> None:
        async with self._session() as session:
            async with session.begin():
                data = await session.execute(select(self.LastBlock))
                last_block = data.scalar()
                if last_block is None:
                    session.add(self.LastBlock(block_number=block_number))
                await session.commit()
    
    async def _process_input_utxo(self, txid: str, vout: int):
        utxo = await self._get_utxo(txid, vout)
        if utxo:
            await self._delete_utxo(txid, vout)
            
    async def _get_utxo_data(self, address: str):
        async with self._session() as session:
            result = await session.execute(select(self.UTXO.tx_id, self.UTXO.output_n, self.UTXO.amount_satoshi).where(self.UTXO.address == address))
            return result.fetchall()
            
    async def _get_utxo(self, tx_id: str, output_n: int):
        async with self._session() as session:
            result = await session.execute(select(self.UTXO).where(self.UTXO.tx_id == tx_id, self.UTXO.output_n == output_n))
            return result.scalar()
            

    async def _delete_utxo(self, tx_id: str, output_n: int):
        async with self._session() as session:
            async with session.begin():
                await session.delete(await session.get(self.UTXO, (tx_id, output_n)))
                await session.commit()

            
    async def _get_last_block(self) -> Optional[int]:
        async with self._session() as session:
            result = await session.execute(select(self.LastBlock.block_number))
            return result.scalar()
            
    async def _get_addresses(self) -> Optional[int]:
        async with self._session() as session:
            result = await session.execute(select(self.Address.address))
            return {row[0] for row in result.fetchall()}