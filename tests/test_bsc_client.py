import os

import pytest
from confest import vcr_c

from aiotx.clients import AioTxBSCClient

node_url = "https://nameless-flashy-snow.bsc-testnet.quiknode.pro/c54e248a38fb9b7a8b31d84d57c1e41b203ed019/"
chain_id = 97
client = AioTxBSCClient(node_url, chain_id)

PRIVATE_KEY_TO_SEND_FROM = os.environ.get("TEST_BSC_WALLET_PRIVATE_KEY")
MAIN_WALLET = client.get_address_from_private_key(PRIVATE_KEY_TO_SEND_FROM)
CONTRACT = "0x337610d27c682E347C9cD60BD4b3b107C9d34dDd"
DESTINATION_ADDRESS = "0xf9E35E4e1CbcF08E99B84d3f6FF662Ba4c306b5a"


@vcr_c.use_cassette("bsc/get_last_block.yaml")
async def test_get_last_block():
    await client.get_last_block()


@pytest.mark.parametrize(
    "wallet_address,",
    [
        (MAIN_WALLET),
        ("0x1284214b9b9c85549aB3D2b972df0dEEf66aC2c9"),
        ("0x3a82a5a2b77d33a12621e860d1d19cdfb8bf63b4"),
        ("0x0e28BD8B2D4efb8A3128f7fB310f4e227E25DB6F"),
        ("0xfb2bdebad0cb9486e714b053a2dbfaf7c05151c9"),
        ("0x040bA056435A7675847F4D577d3Cb8Fc2646A946"),
        ("040bA056435A7675847F4D577d3Cb8Fc2646A946"),
    ],
)
@vcr_c.use_cassette("bsc/get_balance.yaml")
async def test_get_balance(wallet_address):
    await client.get_balance(wallet_address)


@pytest.mark.parametrize(
    "tx_id,",
    [
        ("0x6007710c9bc82da8a9cb6104e39fef7b259df0d257a0efcf46908b9451909118"),
        ("0xdeac5f03c42970ec4c89ec540c886a2738b8b8fc8c415d0bd231ea94dad81727"),
        ("0x26611f5796882c8f45a52c4443c2cda4580ef0bb06d57686d34672207312dfd3"),
        ("0xf82c96662db872899f16ea9dfed73fb7c29f3942fdbfc97500ca071793f5a397"),
        ("0x8a0dc46462919c8a1c15c90e79782ba4e56b9053fad8975c9b6bec094f001895"),
        ("0x41c8e2e03195c29cea37d67ad234d91c52258a514c78f9fcfd196aa5992209ae"),
    ],
)
@vcr_c.use_cassette("bsc/get_transaction.yaml")
async def test_get_transaction(tx_id):
    await client.get_transaction(tx_id)


@pytest.mark.parametrize(
    "wallet_address, contract",
    [
        ("0xf9E35E4e1CbcF08E99B84d3f6FF662Ba4c306b5a", CONTRACT),
        ("0x896c54023265f2c821f241BC694d8A0E1FA7DF2E", CONTRACT),
        ("0x3ffeCb152F95f7122990ab16Eff4B0B5d533497e", CONTRACT),
        ("0x98265f1Dd3224aBA2148C6cF2Ef873b05A3476C1", CONTRACT),
        ("0xf6626A900e4Cc958D2cD0Eb2186Fd6B29EDB63ce", CONTRACT),
        ("0x2dbB5a4c235164B9f772179A43faca2c71a8abDB", CONTRACT),
    ],
)
@vcr_c.use_cassette("bsc/get_token_balance.yaml")
async def test_get_token_balance(wallet_address, contract):
    await client.get_token_balance(wallet_address, contract)


@pytest.mark.parametrize(
    "wallet_address,",
    [
        ("0xf9E35E4e1CbcF08E99B84d3f6FF662Ba4c306b5a"),
        ("0x896c54023265f2c821f241BC694d8A0E1FA7DF2E"),
        ("0x3ffeCb152F95f7122990ab16Eff4B0B5d533497e"),
        ("0x98265f1Dd3224aBA2148C6cF2Ef873b05A3476C1"),
        ("0xf6626A900e4Cc958D2cD0Eb2186Fd6B29EDB63ce"),
        ("0x2dbB5a4c235164B9f772179A43faca2c71a8abDB"),
    ],
)
@vcr_c.use_cassette("bsc/get_transaction_count.yaml")
async def test_get_transaction_count(wallet_address):
    count = await client.get_transaction_count(wallet_address)
    assert isinstance(count, int)


@vcr_c.use_cassette("bsc/send_transaction.yaml")
async def test_send_transaction():
    result = await client.send_transaction(PRIVATE_KEY_TO_SEND_FROM, DESTINATION_ADDRESS, 10000, 5000000000)
    assert isinstance(result, dict)
    assert "result" in result


@vcr_c.use_cassette("bsc/send_token_transaction.yaml")
async def test_send_token_transaction():
    result = await client.send_token_transaction(
        PRIVATE_KEY_TO_SEND_FROM, DESTINATION_ADDRESS, CONTRACT, 1000000000000000000, 1000000000
    )
    assert isinstance(result, str)
    assert result.startswith("0x")
