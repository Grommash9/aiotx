import os

import pytest
from conftest import vcr_c

from aiotx.clients import AioTxETHClient
from aiotx.exceptions import (
    AioTxError,
    InvalidArgumentError,
    ReplacementTransactionUnderpriced,
    TransactionNotFound,
    WrongPrivateKey,
)

POLYGON_WALLET_PRIVATE_KEY = os.environ.get("TEST_POLYGON_WALLET_PRIVATE_KEY")
assert (
    POLYGON_WALLET_PRIVATE_KEY is not None
), "Please provide TEST_POLYGON_WALLET_PRIVATE_KEY"
CONTRACT = "0x0fd9e8d3af1aaee056eb9e802c3a762a667b1904"
DESTINATION_ADDRESS = "0x3ffeCb152F95f7122990ab16Eff4B0B5d533497e"


@vcr_c.use_cassette("polygon/get_last_block.yaml")
async def test_get_last_block(polygon_client: AioTxETHClient):
    block_id = await polygon_client.get_last_block_number()
    assert isinstance(block_id, int)


@vcr_c.use_cassette("polygon/get_chain_id.yaml")
async def test_get_chain_id(polygon_client: AioTxETHClient):
    chain_id = await polygon_client.get_chain_id()
    assert isinstance(chain_id, int)
    assert chain_id == 80002


@pytest.mark.parametrize(
    "wallet_address, expected_exception, expected_balance",
    [
        ("0x56ebc43d764761bc09d5918787672e2c8d46da5f", None, 0),
        ("0xf663792Be0EdD00AFFB8BBe4Ac6d8185efD5671d", None, 25472000000000000),
        ("0xA869aF2883DD6C881bC59594aDfB3e8b136321b4", None, 120000000000000),
        ("0xE27017DD9EF7e3D0A8321C2041Fc4402e89945b6", None, 130000000000000),
        ("0x39832298befa06a6db0c920ada31cfebAD2e33aB", None, 0),
        ("0xC4BfcCb1668d6e464f33a76bAdD8c8d7d341E04B", None, 0),
        ("0x68EfbC84d1Eabc193979beab2E2DDc20B219A14", InvalidArgumentError, 0),
    ],
)
@vcr_c.use_cassette("polygon/get_balance.yaml")
async def test_get_balance(
    polygon_client: AioTxETHClient, wallet_address, expected_exception, expected_balance
):
    if expected_exception:
        with pytest.raises(expected_exception):
            await polygon_client.get_balance(wallet_address)
    else:
        balance = await polygon_client.get_balance(wallet_address)
        assert isinstance(balance, int)
        assert balance == expected_balance


@pytest.mark.parametrize(
    "tx_id, expected_exception",
    [
        ("0x2860ef29c17bf8fd87a8ef4fcd64a76402b70011cba54f7e8ef2eecedf72a08f", None),
        ("0x1913ae3314b38254c07538910ebdf2e3a3d6562b084769ef6614a0f0f4e01367", None),
        ("0x711f485342d60846117686998618a23d148506b08a8f11462c6683a6f37b4845", None),
        ("0xa7c8f80df5559b87a46f881fba25d282f4bb15645211d43ec8531abe75b13cf1", None),
        ("0xea9bd00efa11d22593f3e636f00f8a1a36b836df3f7b4f1d945c1d7bc823bec5", None),
        ("0x75d284a35f58e1a847d5112e157e7bd41fab09feeac63df2f92048c863006cb2", None),
        (
            "0x93ff17f18511c4fa74166a2dbd53ffa7ce5cc2ee431cbb4fd5e02bbdf2701b73",
            TransactionNotFound,
        ),
        (
            "0x93ff17f18511c4fa74166a2dbd53ffa7ce5cc2ee431cbb4fd5e02bbdf2701b2",
            InvalidArgumentError,
        ),
        (
            "0x93ff17f18511c4fa74166a2dbd53ffa7ce5cc2ee431cbb4fd5e02bbdf701b72",
            InvalidArgumentError,
        ),
    ],
)
@vcr_c.use_cassette("polygon/get_transaction.yaml")
async def test_get_transaction(
    polygon_client: AioTxETHClient, tx_id, expected_exception
):
    if expected_exception:
        with pytest.raises(expected_exception):
            await polygon_client.get_transaction(tx_id)
    else:
        tx = await polygon_client.get_transaction(tx_id)
        assert "aiotx_decoded_input" in tx.keys()


@pytest.mark.parametrize(
    "wallet_address, contract, expected_exception, expected_balance",
    [
        (
            "0x3ce3668dfccaee1a348166b2df1c88f0d6a1d2db",
            CONTRACT,
            None,
            38000000000000000000,
        ),
        (
            "0xe68db62564964df789e00927f86b5d6572f77634",
            CONTRACT,
            None,
            25000000000000000000,
        ),
        (
            "0x15331fe7e3638c6edd5833286c7fdceb3506d46c",
            CONTRACT,
            None,
            182000000000000000000,
        ),
        (
            "0x3ce3668dfccaee1a348166b2df1c88f0d6a1d2db",
            CONTRACT,
            None,
            38000000000000000000,
        ),
        (
            "0x94524d4d3b8ad325f48d637b65f83e50165c6bbb",
            CONTRACT,
            None,
            25000000000000000000,
        ),
        (
            "0x440eb4c94b0aaa8bb3e154fa1361adef71f606e0",
            CONTRACT,
            None,
            125000000000000000000,
        ),
        ("0xDA31b5ac94C559478Eeaa7E347ee4557f9a6F71C", CONTRACT, None, 0),
        (
            "0xDA31b5ac94C559478Eeaa7E347ee4557f9a6F71C",
            "Eeaa7E347ee4557f9a6F71C",
            InvalidArgumentError,
            0,
        ),
    ],
)
@vcr_c.use_cassette("polygon/get_token_balance.yaml")
async def test_get_token_balance(
    polygon_client: AioTxETHClient,
    wallet_address,
    contract,
    expected_exception,
    expected_balance,
):
    if expected_exception:
        with pytest.raises(expected_exception):
            await polygon_client.get_contract_balance(wallet_address, contract)
    else:
        balance = await polygon_client.get_contract_balance(wallet_address, contract)
        assert isinstance(balance, int)
        assert expected_balance == balance


@pytest.mark.parametrize(
    "wallet_address, expected_exception, expected_count",
    [
        ("0x3ce3668dfccaee1a348166b2df1c88f0d6a1d2db", None, 19),
        ("0xe68db62564964df789e00927f86b5d6572f77634", None, 0),
        ("0x15331fe7e3638c6edd5833286c7fdceb3506d46c", None, 2),
        ("0x94524d4d3b8ad325f48d637b65f83e50165c6bbb", None, 31),
        ("0x440eb4c94b0aaa8bb3e154fa1361adef71f606e0", None, 4),
        ("0xDA31b5ac94C559478Eeaa7E347ee4557f9a6F71C", None, 0),
        ("0xDA31b5ac94C559478Eeaa7E347ee4557f9a6F71", InvalidArgumentError, 0),
        ("DA31b5ac94C559478Eeaa7E347ee4557f9a6F71C", InvalidArgumentError, 0),
    ],
)
@vcr_c.use_cassette("polygon/get_transaction_count.yaml")
async def test_get_transaction_count(
    polygon_client: AioTxETHClient, wallet_address, expected_exception, expected_count
):
    if expected_exception:
        with pytest.raises(expected_exception):
            await polygon_client.get_transactions_count(wallet_address)
    else:
        count = await polygon_client.get_transactions_count(wallet_address)
        assert isinstance(count, int)
        assert expected_count == count


@vcr_c.use_cassette("polygon/get_gas_price.yaml")
async def test_get_gas_price(polygon_client: AioTxETHClient):
    result = await polygon_client.get_gas_price()
    assert isinstance(result, int)


@pytest.mark.parametrize(
    "private_key, to_address, amount, gas_price, gas_limit, expected_exception",
    [
        (
            "87e6dah15aa076a932cd9f0663da72f8cfb6d3e23c00ef1269104bd904938chd",
            DESTINATION_ADDRESS,
            0.00001,
            5,
            21000,
            WrongPrivateKey,
        ),
        (
            "87e6dah15aa076a932cd9f0663da72f8cfb6d3e23c00ef1269104bd904938ch",
            DESTINATION_ADDRESS,
            0.00001,
            5,
            21000,
            WrongPrivateKey,
        ),
        (
            "e6dah15aa076a932cd9f0663da72f8cfb6d3e23c00ef1269104bd904938chd",
            DESTINATION_ADDRESS,
            0.00001,
            5,
            21000,
            WrongPrivateKey,
        ),
        (
            POLYGON_WALLET_PRIVATE_KEY,
            "0xf9E35E4e1CbcF08E99B84d3f6FF662Ba4c306b5",
            0.00001,
            5,
            21000,
            ValueError,
        ),
        (
            POLYGON_WALLET_PRIVATE_KEY,
            "f9E35E4e1CbcF08E99B84d3f6FF662Ba4c306b5a",
            0.00001,
            5,
            21000,
            None,
        ),
        (
            POLYGON_WALLET_PRIVATE_KEY,
            "0xf9E35E4e1CbcF08E84d3f6FF662Ba4c306b5a",
            0.00001,
            5,
            21000,
            ValueError,
        ),
        (
            POLYGON_WALLET_PRIVATE_KEY,
            DESTINATION_ADDRESS,
            0.00001,
            5,
            21000,
            ReplacementTransactionUnderpriced,
        ),
        (POLYGON_WALLET_PRIVATE_KEY, DESTINATION_ADDRESS, 5, 5, 21000, AioTxError),
        (
            POLYGON_WALLET_PRIVATE_KEY,
            DESTINATION_ADDRESS,
            0.00001,
            0,
            21000,
            AioTxError,
        ),
        (
            POLYGON_WALLET_PRIVATE_KEY,
            DESTINATION_ADDRESS,
            0,
            5,
            21000,
            ReplacementTransactionUnderpriced,
        ),
        (POLYGON_WALLET_PRIVATE_KEY, DESTINATION_ADDRESS, 0.00001, 5, 0, AioTxError),
        (
            POLYGON_WALLET_PRIVATE_KEY,
            DESTINATION_ADDRESS,
            0.00001,
            5,
            61000,
            ReplacementTransactionUnderpriced,
        ),
    ],
)
@vcr_c.use_cassette("polygon/send_transaction.yaml")
async def test_send_transaction(
    polygon_client: AioTxETHClient,
    private_key,
    to_address,
    amount,
    gas_price,
    gas_limit,
    expected_exception,
):
    """
    Here it's raising ReplacementTransactionUnderpriced and NonceTooLowError because we have reusing
    the same VCR data for every get nonce request, we should investigate how we can change that maybe?
    """
    gas_price = polygon_client.to_wei(gas_price, "gwei")
    wei_amount = polygon_client.to_wei(amount, "ether")
    if expected_exception:
        with pytest.raises(expected_exception):
            await polygon_client.send(
                private_key,
                to_address,
                wei_amount,
                gas_price=gas_price,
                gas_limit=gas_limit,
            )
    else:
        result = await polygon_client.send(
            private_key,
            to_address,
            wei_amount,
            gas_price=gas_price,
            gas_limit=gas_limit,
        )
        assert isinstance(result, str)


@pytest.mark.parametrize(
    "private_key, to_address, amount, expected_exception",
    [
        (POLYGON_WALLET_PRIVATE_KEY, DESTINATION_ADDRESS, 0.00001, None),
        (
            POLYGON_WALLET_PRIVATE_KEY,
            "0xf9E35E4e1CbcF08E99B84d3f6FF662Ba4c306b5a",
            0.00001,
            ReplacementTransactionUnderpriced,
        ),
    ],
)
@vcr_c.use_cassette("polygon/send_transaction_with_auto_gas.yaml")
async def test_send_transaction_with_auto_gas(
    polygon_client: AioTxETHClient, private_key, to_address, amount, expected_exception
):
    """
    Here it's raising ReplacementTransactionUnderpriced and NonceTooLowError because we have reusing
    the same VCR data for every get nonce request, we should investigate how we can change that maybe?
    """
    wei_amount = polygon_client.to_wei(amount, "ether")
    if expected_exception:
        with pytest.raises(expected_exception):
            await polygon_client.send(private_key, to_address, wei_amount)
    else:
        result = await polygon_client.send(private_key, to_address, wei_amount)
        assert isinstance(result, str)


@vcr_c.use_cassette("polygon/send_transaction_with_custom_nonce.yaml")
async def test_send_transaction_with_custom_nonce(polygon_client: AioTxETHClient):
    wei_amount = polygon_client.to_wei(0.00001, "ether")
    sender_address = polygon_client.get_address_from_private_key(
        POLYGON_WALLET_PRIVATE_KEY
    )
    nonce = await polygon_client.get_transactions_count(sender_address)
    first_tx = await polygon_client.send(
        POLYGON_WALLET_PRIVATE_KEY, DESTINATION_ADDRESS, wei_amount, nonce=nonce
    )
    assert isinstance(first_tx, str)
    second_tx = await polygon_client.send(
        POLYGON_WALLET_PRIVATE_KEY, sender_address, wei_amount, nonce=nonce + 1
    )
    assert isinstance(second_tx, str)


@pytest.mark.parametrize(
    "contract, expected_decimals, expected_exception",
    [
        (CONTRACT, 18, None),
        ("0x337610d27c682E347C9cD60BD4b3b107C9d34dD", 18, InvalidArgumentError),
        ("0x41E94Eb019C0762f9Bfcf9Fb1E58725BfB0e7582", 6, None),
    ],
)
@vcr_c.use_cassette("polygon/get_contract_decimals.yaml")
async def test_get_contract_decimals(
    polygon_client: AioTxETHClient, contract, expected_decimals, expected_exception
):
    if expected_exception:
        with pytest.raises(expected_exception):
            await polygon_client.get_contract_decimals(contract)
    else:
        decimals = await polygon_client.get_contract_decimals(contract)
        assert decimals == expected_decimals


@vcr_c.use_cassette("polygon/send_token_transaction_with_auto_params.yaml")
async def test_send_transaction_with_auto_params(polygon_client: AioTxETHClient):
    wei_amount = polygon_client.to_wei(0.1, "ether")
    tx_id = await polygon_client.send_token(
        POLYGON_WALLET_PRIVATE_KEY, DESTINATION_ADDRESS, CONTRACT, wei_amount
    )
    assert isinstance(tx_id, str)


@pytest.mark.parametrize(
    "private_key, to_address, contract, amount, gas_price, gas_limit, expected_exception",
    [
        (
            "87e6dah15aa076a932cd9f0663da72f8cfb6d3e23c00ef1269104bd904938chd",
            DESTINATION_ADDRESS,
            CONTRACT,
            1,
            5,
            61000,
            WrongPrivateKey,
        ),
        (
            "87e6dah15aa076a932cd9f0663da72f8cfb6d3e23c00ef1269104bd904938ch",
            DESTINATION_ADDRESS,
            CONTRACT,
            1,
            5,
            61000,
            WrongPrivateKey,
        ),
        (
            "e6dah15aa076a932cd9f0663da72f8cfb6d3e23c00ef1269104bd904938chd",
            DESTINATION_ADDRESS,
            CONTRACT,
            1,
            5,
            61000,
            WrongPrivateKey,
        ),
        (
            POLYGON_WALLET_PRIVATE_KEY,
            "0xf9E35E4e1CbcF08E984d3f6FF662Ba4c306b5a",
            CONTRACT,
            1,
            5,
            61000,
            ValueError,
        ),
        (
            POLYGON_WALLET_PRIVATE_KEY,
            "f9E5E4e1CbcF08E99B84d3f6FF662Ba4c306b5a",
            CONTRACT,
            1,
            5,
            61000,
            ValueError,
        ),
        (
            POLYGON_WALLET_PRIVATE_KEY,
            "0xf9E35E4e1CbcF08E99B84d3f6FF662Ba4c306b",
            CONTRACT,
            1,
            5,
            61000,
            ValueError,
        ),
        (
            POLYGON_WALLET_PRIVATE_KEY,
            DESTINATION_ADDRESS,
            "0xf9E35E4e1CbcF08E984d3f6FF662Ba4c306b5a",
            0.00001,
            5,
            61000,
            ValueError,
        ),
        (
            POLYGON_WALLET_PRIVATE_KEY,
            DESTINATION_ADDRESS,
            "f9E35E4e1CbcF08E99B84d3f6FF662Ba4c306b5a",
            1,
            5,
            61000,
            None,
        ),
        (
            POLYGON_WALLET_PRIVATE_KEY,
            DESTINATION_ADDRESS,
            "0xf9E35E4e1CbcF08E99B84d3f6FF662Ba4c306b",
            1,
            5,
            61000,
            ValueError,
        ),
        (
            POLYGON_WALLET_PRIVATE_KEY,
            DESTINATION_ADDRESS,
            CONTRACT,
            0.3,
            5,
            61000,
            ReplacementTransactionUnderpriced,
        ),
        (
            POLYGON_WALLET_PRIVATE_KEY,
            DESTINATION_ADDRESS,
            CONTRACT,
            1000,
            5,
            61000,
            ReplacementTransactionUnderpriced,
        ),
        (
            POLYGON_WALLET_PRIVATE_KEY,
            DESTINATION_ADDRESS,
            CONTRACT,
            1,
            0,
            61000,
            AioTxError,
        ),
        (
            POLYGON_WALLET_PRIVATE_KEY,
            DESTINATION_ADDRESS,
            CONTRACT,
            0,
            5,
            61000,
            ReplacementTransactionUnderpriced,
        ),
        (
            POLYGON_WALLET_PRIVATE_KEY,
            DESTINATION_ADDRESS,
            CONTRACT,
            1,
            5,
            0,
            AioTxError,
        ),
        (
            POLYGON_WALLET_PRIVATE_KEY,
            DESTINATION_ADDRESS,
            CONTRACT,
            0.4,
            5,
            61000,
            ReplacementTransactionUnderpriced,
        ),
    ],
)
@vcr_c.use_cassette("polygon/send_token_transaction.yaml")
async def test_send_token_transaction(
    polygon_client: AioTxETHClient,
    private_key,
    to_address,
    contract,
    amount,
    gas_price,
    gas_limit,
    expected_exception,
):
    """
    Here it's raising ReplacementTransactionUnderpriced and NonceTooLowError because we have reusing
    the same VCR data for every get nonce request, we should investigate how we can change that maybe?
    """
    gas_price = polygon_client.to_wei(gas_price, "gwei")
    wei_amount = polygon_client.to_wei(amount, "gwei")

    if expected_exception:
        with pytest.raises(expected_exception):
            await polygon_client.send_token(
                private_key,
                to_address,
                contract,
                wei_amount,
                gas_price=gas_price,
                gas_limit=gas_limit,
            )
    else:
        result = await polygon_client.send_token(
            private_key,
            to_address,
            contract,
            wei_amount,
            gas_price=gas_price,
            gas_limit=gas_limit,
        )
        assert isinstance(result, str)


@vcr_c.use_cassette("polygon/send_token_transaction_with_custom_nonce.yaml")
async def test_send_token_transaction_with_custom_nonce(polygon_client: AioTxETHClient):
    wei_amount = polygon_client.to_wei(0.1, "gwei")
    sender_address = polygon_client.get_address_from_private_key(
        POLYGON_WALLET_PRIVATE_KEY
    )
    nonce = await polygon_client.get_transactions_count(sender_address)
    first_tx = await polygon_client.send_token(
        POLYGON_WALLET_PRIVATE_KEY,
        DESTINATION_ADDRESS,
        CONTRACT,
        wei_amount,
        nonce=nonce,
    )
    assert isinstance(first_tx, str)
    second_tx = await polygon_client.send_token(
        POLYGON_WALLET_PRIVATE_KEY,
        sender_address,
        CONTRACT,
        wei_amount,
        nonce=nonce + 1,
    )
    assert isinstance(second_tx, str)
