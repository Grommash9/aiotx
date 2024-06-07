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

PRIVATE_KEY_TO_SEND_FROM = os.environ.get("TEST_ETH_WALLET_PRIVATE_KEY")
assert (
    PRIVATE_KEY_TO_SEND_FROM is not None
), "Please provide TEST_ETH_WALLET_PRIVATE_KEY"
CONTRACT = "0x419Fe9f14Ff3aA22e46ff1d03a73EdF3b70A62ED"
DESTINATION_ADDRESS = "0xD515F5737044238B0f0d6c100109DA44066bE749"


@vcr_c.use_cassette("eth/get_last_block.yaml")
async def test_get_last_block(eth_client: AioTxETHClient):
    block_id = await eth_client.get_last_block_number()
    assert isinstance(block_id, int)


@vcr_c.use_cassette("eth/get_chain_id.yaml")
async def test_get_chain_id(eth_client: AioTxETHClient):
    chain_id = await eth_client.get_chain_id()
    assert isinstance(chain_id, int)
    assert chain_id == 11155111


@pytest.mark.parametrize(
    "wallet_address, expected_exception, expected_balance",
    [
        ("0x56ebc43d764761bc09d5918787672e2c8d46da5f", None, 22243749149992258),
        ("0xf663792Be0EdD00AFFB8BBe4Ac6d8185efD5671d", None, 72596311066831845012),
        ("0xA869aF2883DD6C881bC59594aDfB3e8b136321b4", None, 2360954490480603880),
        ("0xE27017DD9EF7e3D0A8321C2041Fc4402e89945b6", None, 9148320984250803464),
        ("0x39832298befa06a6db0c920ada31cfebAD2e33aB", None, 36026722467628523),
        ("0xC4BfcCb1668d6e464f33a76bAdD8c8d7d341E04B", None, 0),
        ("0x68EfbC84d1Eabc193979beab2E2DDc20B219A14", InvalidArgumentError, 0),
    ],
)
@vcr_c.use_cassette("eth/get_balance.yaml")
async def test_get_balance(
    eth_client: AioTxETHClient, wallet_address, expected_exception, expected_balance
):
    if expected_exception:
        with pytest.raises(expected_exception):
            await eth_client.get_balance(wallet_address)
    else:
        balance = await eth_client.get_balance(wallet_address)
        assert isinstance(balance, int)
        assert balance == expected_balance


@pytest.mark.parametrize(
    "tx_id, expected_exception",
    [
        ("0x293fbb7d14e6a11a152fad9d621abdf810acfccb7c8c95977622223638fad96a", None),
        ("0x0d03e84a4d1673b590885ec270553fbd310620debd12d1779796e9ff181f66fe", None),
        ("0x82e8a1058cdadcd0cd728388c48456db7e79051a198d654de85a7f51bf326fb8", None),
        ("0x2f88aa536f9ef65087ce0e81918febf65396cf4a8ff5d535d58a45de4a13d076", None),
        ("0xcb5ad4fd610b6e9e687b5154f4832c0233a527719dcfad6d47500c9f3a50f7cc", None),
        ("0x93ff17f18511c4fa74166a2dbd53ffa7ce5cc2ee431cbb4fd5e02bbdf2701b72", None),
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
@vcr_c.use_cassette("eth/get_transaction.yaml")
async def test_get_transaction(eth_client: AioTxETHClient, tx_id, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            await eth_client.get_transaction(tx_id)
    else:
        tx = await eth_client.get_transaction(tx_id)
        assert "aiotx_decoded_input" in tx.keys()


@pytest.mark.parametrize(
    "wallet_address, contract, expected_exception, expected_balance",
    [
        ("0x159bD467fafcfA348D2b5f357b23aA1d70E814A0", CONTRACT, None, 10109029605),
        ("0x265253254239F1ce54B2580d6Bfa39Afe41D545A", CONTRACT, None, 1665000000),
        ("0xAf0Eca5c36b0380f27412155f6e59618a38e778F", CONTRACT, None, 14000000000),
        ("0x85213732c4F14EaB4B00eB1960a29077302CF131", CONTRACT, None, 12500000000),
        ("0x9cd384d1Dc5Ba08234aE8D57b0d43724caE8C4d6", CONTRACT, None, 11200000000),
        ("0x42827369CD85aD4E88d93D482C144803Aca448C1", CONTRACT, None, 11000000000),
        ("0xDA31b5ac94C559478Eeaa7E347ee4557f9a6F71C", CONTRACT, None, 0),
        (
            "0xDA31b5ac94C559478Eeaa7E347ee4557f9a6F71C",
            "Eeaa7E347ee4557f9a6F71C",
            InvalidArgumentError,
            0,
        ),
    ],
)
@vcr_c.use_cassette("eth/get_token_balance.yaml")
async def test_get_token_balance(
    eth_client: AioTxETHClient,
    wallet_address,
    contract,
    expected_exception,
    expected_balance,
):
    if expected_exception:
        with pytest.raises(expected_exception):
            await eth_client.get_contract_balance(wallet_address, contract)
    else:
        balance = await eth_client.get_contract_balance(wallet_address, contract)
        assert isinstance(balance, int)
        assert expected_balance == balance


@pytest.mark.parametrize(
    "wallet_address, expected_exception, expected_count",
    [
        ("0x159bD467fafcfA348D2b5f357b23aA1d70E814A0", None, 1),
        ("0x265253254239F1ce54B2580d6Bfa39Afe41D545A", None, 2317),
        ("0xAf0Eca5c36b0380f27412155f6e59618a38e778F", None, 358),
        ("0x85213732c4F14EaB4B00eB1960a29077302CF131", None, 809),
        ("0x9cd384d1Dc5Ba08234aE8D57b0d43724caE8C4d6", None, 902),
        ("0xDA31b5ac94C559478Eeaa7E347ee4557f9a6F71C", None, 0),
        ("0xDA31b5ac94C559478Eeaa7E347ee4557f9a6F71", InvalidArgumentError, 0),
        ("DA31b5ac94C559478Eeaa7E347ee4557f9a6F71C", InvalidArgumentError, 0),
    ],
)
@vcr_c.use_cassette("eth/get_transaction_count.yaml")
async def test_get_transaction_count(
    eth_client: AioTxETHClient, wallet_address, expected_exception, expected_count
):
    if expected_exception:
        with pytest.raises(expected_exception):
            await eth_client.get_transactions_count(wallet_address)
    else:
        count = await eth_client.get_transactions_count(wallet_address)
        assert isinstance(count, int)
        assert expected_count == count


@vcr_c.use_cassette("eth/get_gas_price.yaml")
async def test_get_gas_price(eth_client: AioTxETHClient):
    result = await eth_client.get_gas_price()
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
            PRIVATE_KEY_TO_SEND_FROM,
            "0xf9E35E4e1CbcF08E99B84d3f6FF662Ba4c306b5",
            0.00001,
            5,
            21000,
            ValueError,
        ),
        (
            PRIVATE_KEY_TO_SEND_FROM,
            "f9E35E4e1CbcF08E99B84d3f6FF662Ba4c306b5a",
            0.00001,
            5,
            21000,
            None,
        ),
        (
            PRIVATE_KEY_TO_SEND_FROM,
            "0xf9E35E4e1CbcF08E84d3f6FF662Ba4c306b5a",
            0.00001,
            5,
            21000,
            ValueError,
        ),
        (
            PRIVATE_KEY_TO_SEND_FROM,
            DESTINATION_ADDRESS,
            0.00001,
            5,
            21000,
            ReplacementTransactionUnderpriced,
        ),
        (PRIVATE_KEY_TO_SEND_FROM, DESTINATION_ADDRESS, 5, 5, 21000, AioTxError),
        (PRIVATE_KEY_TO_SEND_FROM, DESTINATION_ADDRESS, 0.00001, 0, 21000, AioTxError),
        (
            PRIVATE_KEY_TO_SEND_FROM,
            DESTINATION_ADDRESS,
            0,
            5,
            21000,
            ReplacementTransactionUnderpriced,
        ),
        (PRIVATE_KEY_TO_SEND_FROM, DESTINATION_ADDRESS, 0.00001, 5, 0, AioTxError),
        (
            PRIVATE_KEY_TO_SEND_FROM,
            DESTINATION_ADDRESS,
            0.00001,
            5,
            61000,
            ReplacementTransactionUnderpriced,
        ),
    ],
)
@vcr_c.use_cassette("eth/send_transaction.yaml")
async def test_send_transaction(
    eth_client: AioTxETHClient,
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
    gas_price = eth_client.to_wei(gas_price, "gwei")
    wei_amount = eth_client.to_wei(amount, "ether")
    if expected_exception:
        with pytest.raises(expected_exception):
            await eth_client.send(
                private_key,
                to_address,
                wei_amount,
                gas_price=gas_price,
                gas_limit=gas_limit,
            )
    else:
        result = await eth_client.send(
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
        (PRIVATE_KEY_TO_SEND_FROM, DESTINATION_ADDRESS, 0.00001, None),
        (
            PRIVATE_KEY_TO_SEND_FROM,
            "0xf9E35E4e1CbcF08E99B84d3f6FF662Ba4c306b5a",
            0.00001,
            ReplacementTransactionUnderpriced,
        ),
    ],
)
@vcr_c.use_cassette("eth/send_transaction_with_auto_gas.yaml")
async def test_send_transaction_with_auto_gas(
    eth_client: AioTxETHClient, private_key, to_address, amount, expected_exception
):
    """
    Here it's raising ReplacementTransactionUnderpriced and NonceTooLowError because we have reusing
    the same VCR data for every get nonce request, we should investigate how we can change that maybe?
    """
    wei_amount = eth_client.to_wei(amount, "ether")
    if expected_exception:
        with pytest.raises(expected_exception):
            await eth_client.send(private_key, to_address, wei_amount)
    else:
        result = await eth_client.send(private_key, to_address, wei_amount)
        assert isinstance(result, str)


@vcr_c.use_cassette("eth/send_transaction_with_custom_nonce.yaml")
async def test_send_transaction_with_custom_nonce(eth_client: AioTxETHClient):
    wei_amount = eth_client.to_wei(0.00001, "ether")
    sender_address = eth_client.get_address_from_private_key(PRIVATE_KEY_TO_SEND_FROM)
    nonce = await eth_client.get_transactions_count(sender_address)
    first_tx = await eth_client.send(
        PRIVATE_KEY_TO_SEND_FROM, DESTINATION_ADDRESS, wei_amount, nonce=nonce
    )
    assert isinstance(first_tx, str)
    second_tx = await eth_client.send(
        PRIVATE_KEY_TO_SEND_FROM, sender_address, wei_amount, nonce=nonce + 1
    )
    assert isinstance(second_tx, str)


@pytest.mark.parametrize(
    "contract, expected_decimals, expected_exception",
    [
        (CONTRACT, 6, None),
        ("0x337610d27c682E347C9cD60BD4b3b107C9d34dD", 18, InvalidArgumentError),
        ("0x1a0cdabee2c57c965b8bbc037671e458805dfdd5", 18, None),
    ],
)
@vcr_c.use_cassette("eth/get_contract_decimals.yaml")
async def test_get_contract_decimals(
    eth_client: AioTxETHClient, contract, expected_decimals, expected_exception
):
    if expected_exception:
        with pytest.raises(expected_exception):
            await eth_client.get_contract_decimals(contract)
    else:
        decimals = await eth_client.get_contract_decimals(contract)
        assert decimals == expected_decimals


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
            PRIVATE_KEY_TO_SEND_FROM,
            "0xf9E35E4e1CbcF08E984d3f6FF662Ba4c306b5a",
            CONTRACT,
            1,
            5,
            61000,
            ValueError,
        ),
        (
            PRIVATE_KEY_TO_SEND_FROM,
            "f9E5E4e1CbcF08E99B84d3f6FF662Ba4c306b5a",
            CONTRACT,
            1,
            5,
            61000,
            ValueError,
        ),
        (
            PRIVATE_KEY_TO_SEND_FROM,
            "0xf9E35E4e1CbcF08E99B84d3f6FF662Ba4c306b",
            CONTRACT,
            1,
            5,
            61000,
            ValueError,
        ),
        (
            PRIVATE_KEY_TO_SEND_FROM,
            DESTINATION_ADDRESS,
            "0xf9E35E4e1CbcF08E984d3f6FF662Ba4c306b5a",
            0.00001,
            5,
            61000,
            ValueError,
        ),
        (
            PRIVATE_KEY_TO_SEND_FROM,
            DESTINATION_ADDRESS,
            "f9E35E4e1CbcF08E99B84d3f6FF662Ba4c306b5a",
            1,
            5,
            61000,
            None,
        ),
        (
            PRIVATE_KEY_TO_SEND_FROM,
            DESTINATION_ADDRESS,
            "0xf9E35E4e1CbcF08E99B84d3f6FF662Ba4c306b",
            1,
            5,
            61000,
            ValueError,
        ),
        (
            PRIVATE_KEY_TO_SEND_FROM,
            DESTINATION_ADDRESS,
            CONTRACT,
            1,
            5,
            61000,
            ReplacementTransactionUnderpriced,
        ),
        (
            PRIVATE_KEY_TO_SEND_FROM,
            DESTINATION_ADDRESS,
            CONTRACT,
            1000,
            5,
            61000,
            ReplacementTransactionUnderpriced,
        ),
        (
            PRIVATE_KEY_TO_SEND_FROM,
            DESTINATION_ADDRESS,
            CONTRACT,
            1,
            0,
            61000,
            AioTxError,
        ),
        (
            PRIVATE_KEY_TO_SEND_FROM,
            DESTINATION_ADDRESS,
            CONTRACT,
            0,
            5,
            61000,
            ReplacementTransactionUnderpriced,
        ),
        (PRIVATE_KEY_TO_SEND_FROM, DESTINATION_ADDRESS, CONTRACT, 1, 5, 0, AioTxError),
        (
            PRIVATE_KEY_TO_SEND_FROM,
            DESTINATION_ADDRESS,
            CONTRACT,
            1,
            5,
            61000,
            ReplacementTransactionUnderpriced,
        ),
    ],
)
@vcr_c.use_cassette("eth/send_token_transaction.yaml")
async def test_send_token_transaction(
    eth_client: AioTxETHClient,
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
    gas_price = eth_client.to_wei(gas_price, "gwei")
    wei_amount = eth_client.to_wei(amount, "mwei")

    if expected_exception:
        with pytest.raises(expected_exception):
            await eth_client.send_token(
                private_key,
                to_address,
                contract,
                wei_amount,
                gas_price=gas_price,
                gas_limit=gas_limit,
            )
    else:
        result = await eth_client.send_token(
            private_key,
            to_address,
            contract,
            wei_amount,
            gas_price=gas_price,
            gas_limit=gas_limit,
        )
        assert isinstance(result, str)


@vcr_c.use_cassette("eth/send_token_transaction_with_custom_nonce.yaml")
async def test_send_token_transaction_with_custom_nonce(eth_client: AioTxETHClient):
    wei_amount = eth_client.to_wei(0.00001, "mwei")
    sender_address = eth_client.get_address_from_private_key(PRIVATE_KEY_TO_SEND_FROM)
    nonce = await eth_client.get_transactions_count(sender_address)
    first_tx = await eth_client.send_token(
        PRIVATE_KEY_TO_SEND_FROM, DESTINATION_ADDRESS, CONTRACT, wei_amount, nonce=nonce
    )
    assert isinstance(first_tx, str)
    second_tx = await eth_client.send_token(
        PRIVATE_KEY_TO_SEND_FROM, sender_address, CONTRACT, wei_amount, nonce=nonce + 1
    )
    assert isinstance(second_tx, str)


@vcr_c.use_cassette("eth/send_token_transaction_with_auto_params.yaml")
async def test_send_transaction_with_auto_params(eth_client: AioTxETHClient):
    wei_amount = eth_client.to_wei(0.00001, "mwei")
    tx_id = await eth_client.send_token(
        PRIVATE_KEY_TO_SEND_FROM, DESTINATION_ADDRESS, CONTRACT, wei_amount
    )
    assert isinstance(tx_id, str)
