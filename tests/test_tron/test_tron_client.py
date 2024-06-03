import pytest
from conftest import vcr_c

from aiotx.clients import AioTxTRONClient
from aiotx.exceptions import (
    InvalidArgumentError,
    RpcConnectionError,
    TransactionNotFound,
)

CONTRACT = "TXLAQ63Xg1NAzckPwKHvzw7CSEmLMEqcdj"

async def test_wallet_generator_convertor(tron_client: AioTxTRONClient):
    wallet = tron_client.generate_address()
    print("wallet", wallet)

    base_58_from_hex = tron_client.hex_address_to_base58(wallet["hex_address"])
    hex_from_base58 = tron_client.base58_to_hex_address(wallet["base58check_address"])

    wallet_from_key = tron_client.get_address_from_private_key(wallet["private_key"])

    assert wallet == wallet_from_key
    assert base_58_from_hex == wallet["base58check_address"]
    assert hex_from_base58 == wallet["hex_address"]


@vcr_c.use_cassette("tron/get_last_block.yaml")
async def test_get_last_block(tron_client: AioTxTRONClient):
    block_id = await tron_client.get_last_block_number()
    assert isinstance(block_id, int)


@vcr_c.use_cassette("tron/get_chain_id.yaml")
async def test_get_chain_id(tron_client: AioTxTRONClient):
    chain_id = await tron_client.get_chain_id()
    assert isinstance(chain_id, int)
    assert chain_id == 3448148188


@pytest.mark.parametrize(
    "wallet_address, expected_exception, expected_balance",
    [
        ("TEZQQ5BXq3nFKUFJknoV15CW24twzH81La", None, 4001000000),
        ("TCnvuKGHUjjx6z4YAoUtCopXA8pXzv16YZ", None, 2892750560),
        ("TX9ctsGJSx8LniV1JgPuvNkXdTGrDdyZqt", None, 390613840),
        ("TXLnrKzcnTqPDiRYgECNMCC37wKgMvZkKU", None, 61477500),
        ("TGYycKuwtyJ1zRt196PhaWfPuUPGr1wi2P", None, 23520),
        ("TAhMH42Mr61MRLkbEpT1vjbXpsKSXBtHRz", None, 0),
        ("TWkcsRj1FnAXA1HzWZEW93hdoQxQ2YXFN", ValueError, 0),
    ],
)
@vcr_c.use_cassette("tron/get_balance.yaml")
async def test_get_balance(tron_client: AioTxTRONClient, wallet_address, expected_exception, expected_balance):
    if expected_exception:
        with pytest.raises(expected_exception):
            await tron_client.get_balance(wallet_address)
    else:
        balance = await tron_client.get_balance(wallet_address)
        assert isinstance(balance, int)
        assert balance == expected_balance


@pytest.mark.parametrize(
    "tx_id, expected_exception",
    [
        ("a7969308be486dcbd5bc16f9a9e750249f1ce4ff5ad36693cd56a8aa81159df8", None),
        ("83033077a7a5ea6e07fa1e36069886daf3abe8bae4e12168391db9c0b28002a7", None),
        ("28777a1b17916030c99a3da3b88e399c11abe3cbbc9e1319e2d2edd83d2810c8", None),
        ("301684ded91391888927f4c3761af0ad76659ede03033fd12c20754e6bc69821", None),
        ("603d90143f388737fa0c57976650301fb493ef19c513c9076099335d0038f2ee", None),
        ("0820f27e5a67ee3443d0b4a60a1f6c6625328b074dedc2f17c0ea8c44ea440e5", None),
        ("0820f27e5a67ee3443d0b4a60a1f6c6625328b074dedc2f17c0ea8c44ea440e6", TransactionNotFound),
        ("0x93ff17f18511c4fa74166a2dbd53ffa7ce5cc2ee431cbb4fd5e02bbdf2701b2", InvalidArgumentError),
        ("0x93ff17f18511c4fa74166a2dbd53ffa7ce5cc2ee431cbb4fd5e02bbdf701b72", InvalidArgumentError),
    ],
)
@vcr_c.use_cassette("tron/get_transaction.yaml")
async def test_get_transaction(tron_client: AioTxTRONClient, tx_id, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            await tron_client.get_transaction(tx_id)
    else:
        tx = await tron_client.get_transaction(tx_id)
        assert "aiotx_decoded_input" in tx.keys()


@pytest.mark.parametrize(
    "wallet_address, contract, expected_exception, expected_balance",
    [
        ("TEZQQ5BXq3nFKUFJknoV15CW24twzH81La", CONTRACT, None, 50000000000),
        ("TCnvuKGHUjjx6z4YAoUtCopXA8pXzv16YZ", CONTRACT, None, 163489214426),
        ("TX9ctsGJSx8LniV1JgPuvNkXdTGrDdyZqt", CONTRACT, None, 0),
        ("TXLnrKzcnTqPDiRYgECNMCC37wKgMvZkKU", CONTRACT, None, 49845248),
        ("TGYycKuwtyJ1zRt196PhaWfPuUPGr1wi2P", CONTRACT, None, 0),
        ("TGYycKuwtyJ1zRt196PhaWfPuUPGr1wi2D", CONTRACT, ValueError, 0),
        ("TAhMH42Mr61MRLkbEpT1vjbXpsKSXBtHRz", CONTRACT, None, 0),
        ("0xDA31b5ac94C559478Eeaa7E347ee4557f9a6F71C", "Eeaa7E347ee4557f9a6F71C", InvalidArgumentError, 0),
    ],
)
@vcr_c.use_cassette("tron/get_token_balance.yaml")
async def test_get_token_balance(
    tron_client: AioTxTRONClient, wallet_address, contract, expected_exception, expected_balance
):

    if expected_exception:
        with pytest.raises(expected_exception):
            await tron_client.get_contract_balance(wallet_address, contract)
    else:
        balance = await tron_client.get_contract_balance(wallet_address, contract)
        assert isinstance(balance, int)
        assert expected_balance == balance


@pytest.mark.parametrize(
    "contract, expected_decimals, expected_exception",
    [
        (CONTRACT, 6, None),
        ("TVSvjZdyDSNocHm7dP3jvCmMNsCnMTPa5W", 18, None),
        ("TSos1xxjqMrGKBxycVmtgrnFvv9M6FDFUX", 9, RpcConnectionError),
    ],
)
@vcr_c.use_cassette("tron/get_contract_decimals.yaml")
async def test_get_contract_decimals(tron_client: AioTxTRONClient, contract, expected_decimals, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            await tron_client.get_contract_decimals(contract)
    else:
        decimals = await tron_client.get_contract_decimals(contract)
        assert decimals == expected_decimals


@vcr_c.use_cassette("tron/get_block_by_number.yaml")
async def test_get_block_by_number(tron_client: AioTxTRONClient):
    block = await tron_client.get_block_by_number(47391985)
    assert isinstance(block, dict)

    assert block["hash"] == "0x0000000002d324f19381c09aa2574e0c1f87a36af924e892e2475338b312ed1b"

    tx_hashes = [tx["hash"] for tx in block["transactions"]]
    assert "0x7262767a999d16cca97807f46e5aac6a8c970b6525e06b49324fb5bfa686bd74" in tx_hashes
    assert "0x2b428b49d2cc2ed2e64e623b570f0478a77aab6d84c5183c200b538a31de017c" in tx_hashes
    assert "0xc69e7d35976989648b88376d82e45a17f35ff441e411cbfc1d3bd86085a10900" in tx_hashes
