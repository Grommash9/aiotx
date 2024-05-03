import os

import pytest
from confest import bsc_client, vcr_c  # noqa

from aiotx.clients import AioTxBSCClient
from aiotx.exceptions import (
    InvalidArgumentError,
    TransactionNotFound,
)

PRIVATE_KEY_TO_SEND_FROM = os.environ.get("TEST_BSC_WALLET_PRIVATE_KEY")
assert PRIVATE_KEY_TO_SEND_FROM is not None, "Please provide TEST_BSC_WALLET_PRIVATE_KEY"
CONTRACT = "0x337610d27c682E347C9cD60BD4b3b107C9d34dDd"
DESTINATION_ADDRESS = "0xf9E35E4e1CbcF08E99B84d3f6FF662Ba4c306b5a"


@vcr_c.use_cassette("bsc/get_last_block.yaml")
async def test_get_last_block(bsc_client: AioTxBSCClient):
    block_id = await bsc_client.get_last_block()
    assert isinstance(block_id, int)

@pytest.mark.parametrize(
    "wallet_address, expected_exception, expected_balance",
    [
        ("0x1284214b9b9c85549aB3D2b972df0dEEf66aC2c9", None, 10561622435613231665),
        ("0x3a82a5a2b77d33a12621e860d1d19cdfb8bf63b4", None, 99724094999968300),
        ("0x0e28BD8B2D4efb8A3128f7fB310f4e227E25DB6F", None, 691239109999999988),
        ("0xfb2bdebad0cb9486e714b053a2dbfaf7c05151c9", None, 271930000000000),
        ("0x040bA056435A7675847F4D577d3Cb8Fc2646A946", None, 421930000000000),
        ("0x040bA056435A7675847F4D577d3Cb8Fc2646A948", None, 0),
        ("040bA056435A7675847F4D577d3Cb8Fc2646A946", InvalidArgumentError, 0),
    ],
)
@vcr_c.use_cassette("bsc/get_balance.yaml")
async def test_get_balance(bsc_client: AioTxBSCClient, wallet_address, expected_exception, expected_balance):
    if expected_exception:
        with pytest.raises(expected_exception):
            await bsc_client.get_balance(wallet_address)
    else:
        balance = await bsc_client.get_balance(wallet_address)
        assert isinstance(balance, int)
        assert balance == expected_balance


@pytest.mark.parametrize(
    "tx_id, expected_exception",
    [
        ("0x6007710c9bc82da8a9cb6104e39fef7b259df0d257a0efcf46908b9451909118", None),
        ("0xdeac5f03c42970ec4c89ec540c886a2738b8b8fc8c415d0bd231ea94dad81727", None),
        ("0x26611f5796882c8f45a52c4443c2cda4580ef0bb06d57686d34672207312dfd3", None),
        ("0xf82c96662db872899f16ea9dfed73fb7c29f3942fdbfc97500ca071793f5a397", None),
        ("0x8a0dc46462919c8a1c15c90e79782ba4e56b9053fad8975c9b6bec094f001895", None),
        ("0x41c8e2e03195c29cea37d67ad234d91c52258a514c78f9fcfd196aa5992209ae", None),
        ("0x6007710c9bc82da8a9cb6104e39fef7b259df0d257a0efcf46908b9451909111", TransactionNotFound),
        ("0x6007710c9bc82da8a9cb6104e39fef7b259df0d257a0efcf46908b945190911", InvalidArgumentError),
        ("41c8e2e03195c29cea37d67ad234d91c52258a514c78f9fcfd196aa5992209ae", InvalidArgumentError),

    ],
)
@vcr_c.use_cassette("bsc/get_transaction.yaml")
async def test_get_transaction(bsc_client: AioTxBSCClient, tx_id, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            await bsc_client.get_transaction(tx_id)
    else:
        tx = await bsc_client.get_transaction(tx_id)
        assert "aiotx_decoded_input" in tx.keys()



@pytest.mark.parametrize(
    "wallet_address, contract, expected_exception, expected_balance",
    [
        ("0xf9E35E4e1CbcF08E99B84d3f6FF662Ba4c306b5a", CONTRACT, None, 1000000001000000000),
        ("0x896c54023265f2c821f241BC694d8A0E1FA7DF2E", CONTRACT, None, 3570000000000000000),
        ("0x3ffeCb152F95f7122990ab16Eff4B0B5d533497e", CONTRACT, None, 15469999999000000000),
        ("0x98265f1Dd3224aBA2148C6cF2Ef873b05A3476C1", CONTRACT, None, 629546202581319287241),
        ("0xf6626A900e4Cc958D2cD0Eb2186Fd6B29EDB63ce", CONTRACT, None, 950000000000000000),
        ("0x2dbB5a4c235164B9f772179A43faca2c71a8abDB", CONTRACT, None, 32963423288412440122),
        ("0xDA31b5ac94C559478Eeaa7E347ee4557f9a6F71C", CONTRACT, None, 0),
        ("0xDA31b5ac94C559478Eeaa7E347ee4557f9a6F71C", "Eeaa7E347ee4557f9a6F71C", InvalidArgumentError, 0),
    ],
)
@vcr_c.use_cassette("bsc/get_token_balance.yaml")
async def test_get_token_balance(bsc_client: AioTxBSCClient, wallet_address, contract, expected_exception, expected_balance):
    
    if expected_exception:
        with pytest.raises(expected_exception):
            await bsc_client.get_token_balance(wallet_address, contract)
    else:
        balance = await bsc_client.get_token_balance(wallet_address, contract)
        assert isinstance(balance, int)
        assert expected_balance == balance


@pytest.mark.parametrize(
    "wallet_address, expected_exception, expected_count",
    [
        ("0xf9E35E4e1CbcF08E99B84d3f6FF662Ba4c306b5a", None, 0),
        ("0x896c54023265f2c821f241BC694d8A0E1FA7DF2E", None, 0),
        ("0x3ffeCb152F95f7122990ab16Eff4B0B5d533497e", None, 102),
        ("0x98265f1Dd3224aBA2148C6cF2Ef873b05A3476C1", None, 1751),
        ("0xf6626A900e4Cc958D2cD0Eb2186Fd6B29EDB63ce", None, 17),
        ("0x2dbB5a4c235164B9f772179A43faca2c71a8abDB", None, 1),
        ("2dbB5a4c235164B9f772179A43faca2c71a8abDB", InvalidArgumentError, 0),
        ("0x2dbB5a4c235164B9f772179A43faca2c71a8ab", InvalidArgumentError, 0),
    ],
)
@vcr_c.use_cassette("bsc/get_transaction_count.yaml")
async def test_get_transaction_count(bsc_client: AioTxBSCClient, wallet_address, expected_exception, expected_count):
    if expected_exception:
        with pytest.raises(expected_exception):
            await bsc_client.get_transaction_count(wallet_address)
    else:
        count = await bsc_client.get_transaction_count(wallet_address)
        assert isinstance(count, int)
        assert expected_count == count


@vcr_c.use_cassette("bsc/send_transaction.yaml")
async def test_send_transaction(bsc_client: AioTxBSCClient):
    result = await bsc_client.send_transaction(PRIVATE_KEY_TO_SEND_FROM, DESTINATION_ADDRESS, 10000, 5000000000)
    assert isinstance(result, dict)
    assert "result" in result


@vcr_c.use_cassette("bsc/send_token_transaction.yaml")
async def test_send_token_transaction(bsc_client: AioTxBSCClient):
    result = await bsc_client.send_token_transaction(
        PRIVATE_KEY_TO_SEND_FROM, DESTINATION_ADDRESS, CONTRACT, 1000000000000000000, 1000000000
    )
    assert isinstance(result, str)
    assert result.startswith("0x")


@vcr_c.use_cassette("bsc/get_gas_price.yaml")
async def test_send_token_transaction(bsc_client: AioTxBSCClient):
    result = await bsc_client.get_gas_price()
    assert isinstance(result, int)
    assert result == 5000000000
