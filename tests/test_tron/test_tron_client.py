import os

import pytest
from conftest import vcr_c

from aiotx.clients import AioTxTRONClient
from aiotx.exceptions import (
    CreateTransactionError,
    InvalidArgumentError,
    RpcConnectionError,
    TransactionNotFound,
)

TRON_TEST_WALLET_PRIVATE_KEY = os.environ.get("TRON_TEST_WALLET_PRIVATE_KEY")
assert (
    TRON_TEST_WALLET_PRIVATE_KEY is not None
), "Please provide TRON_TEST_WALLET_PRIVATE_KEY"
CONTRACT = "TG3XXyExBkPp9nzdajDZsozEu4BkaSJozs"
DESTINATION_ADDRESS = "TYge3Gid6vVaQvnPVRJ6SVwzC64cw2eBkN"


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
    assert chain_id == 2494104990


@pytest.mark.parametrize(
    "wallet_address, expected_exception, expected_balance",
    [
        ("TFJfLNUX2xbxrmV3YKt8mQJ3vNT6U6Pnc5", None, 2078288163),
        ("TTfKxPqHXDuPsXM7i5oR6uSS8gH2W1UFT7", None, 7058424560),
        ("TMBS8e3toASGy3zgnpgv67rEXXzpiQa9VN", None, 5221937700),
        ("TG8rTPRYkdgYBDi794PK5GGudAP5mMWLye", None, 887415410180),
        ("TGc3KVY27X9gUb5EH9kwbgr9VUv1BxXq5L", None, 99983900000),
        ("TAhMH42Mr61MRLkbEpT1vjbXpsKSXBtHRz", None, 0),
        ("TWkcsRj1FnAXA1HzWZEW93hdoQxQ2YXFN", ValueError, 0),
    ],
)
@vcr_c.use_cassette("tron/get_balance.yaml")
async def test_get_balance(
    tron_client: AioTxTRONClient, wallet_address, expected_exception, expected_balance
):
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
        ("5590fe214bfd566bdf35b19bea05a4392e895fe114102c162576200c3c2b3fba", None),
        ("af267a574245393ee68eac6e9d66f1f109b1e06b825743ff645e1b561d654364", None),
        ("101187c488a251ac092f846f16ec190ae4e7230a029716e2a4fdeb10e720b3f9", None),
        ("8a9247c3db7073298463285fabc9150041b2dc5e19e79a955211e0953e3e6bc9", None),
        ("579d94e7f8131b53aac2634426dca3a6d84950ce44512092d599cae7f331ae09", None),
        ("d695d2917e138edb0407ae77109072e43998c2dd6c68be229c62aa49f0dc43ac", None),
        (
            "0820f27e5a67ee3443d0b4a60a1f6c6625328b074dedc2f17c0ea8c44ea440e6",
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
        ("TSNEe5Tf4rnc9zPMNXfaTF5fZfHDDH8oyW", CONTRACT, None, 9858604795634258),
        ("TT5ZmVgbxiPyixb5Y99F4i5vcDygwH1mPm", CONTRACT, None, 88405001000000),
        ("TX9ctsGJSx8LniV1JgPuvNkXdTGrDdyZqt", CONTRACT, None, 0),
        ("TQkqTUS8iTPmRHHA3rQf1bLCoe9DqZVhsR", CONTRACT, None, 1500000000000),
        ("TGYycKuwtyJ1zRt196PhaWfPuUPGr1wi2P", CONTRACT, None, 0),
        ("TGYycKuwtyJ1zRt196PhaWfPuUPGr1wi2D", CONTRACT, ValueError, 0),
        ("TAhMH42Mr61MRLkbEpT1vjbXpsKSXBtHRz", CONTRACT, None, 0),
        (
            "0xDA31b5ac94C559478Eeaa7E347ee4557f9a6F71C",
            "Eeaa7E347ee4557f9a6F71C",
            InvalidArgumentError,
            0,
        ),
    ],
)
@vcr_c.use_cassette("tron/get_token_balance.yaml")
async def test_get_token_balance(
    tron_client: AioTxTRONClient,
    wallet_address,
    contract,
    expected_exception,
    expected_balance,
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
        ("TB5NSkyzxkzi3eHW87NwFE6TmtTmnZw61y", 6, None),
        ("TSos1xxjqMrGKBxycVmtgrnFvv9M6FDFUX", 9, RpcConnectionError),
    ],
)
@vcr_c.use_cassette("tron/get_contract_decimals.yaml")
async def test_get_contract_decimals(
    tron_client: AioTxTRONClient, contract, expected_decimals, expected_exception
):
    if expected_exception:
        with pytest.raises(expected_exception):
            await tron_client.get_contract_decimals(contract)
    else:
        decimals = await tron_client.get_contract_decimals(contract)
        assert decimals == expected_decimals


@vcr_c.use_cassette("tron/get_block_by_number.yaml")
async def test_get_block_by_number(tron_client: AioTxTRONClient):
    block = await tron_client.get_block_by_number(44739224)
    assert isinstance(block, dict)

    assert (
        block["hash"]
        == "0x0000000002aaaa98ab6a708d8c1ce596055a222059983895733031582fc5563e"
    )

    tx_hashes = [tx["hash"] for tx in block["transactions"]]
    assert (
        "0x98f419efccbcfef53bafac52f85b4083c1092c72b7324156a0ce4882706065e8"
        in tx_hashes
    )
    assert (
        "0x1e580e6a15956bdf39df75728ca658cc868b4a321399c95af81bf15e8dc47a13"
        in tx_hashes
    )


@pytest.mark.parametrize(
    "amount, memo, send_to, private_key, expected_exception, expected_tx_id",
    [
        (
            1,
            "",
            DESTINATION_ADDRESS,
            TRON_TEST_WALLET_PRIVATE_KEY,
            None,
            "53a4f1ef3614b49c530708c109556246bc87faab6d34a428e77c0419ea940041",
        ),
        (1, 5, DESTINATION_ADDRESS, TRON_TEST_WALLET_PRIVATE_KEY, TypeError, ""),
        (
            5,
            "orp3uhg$£(TUP42t38P(HU$h3r5g8))",
            DESTINATION_ADDRESS,
            TRON_TEST_WALLET_PRIVATE_KEY,
            None,
            "06227edc693ed47962d1789fecf6bab84fe9fe8d9961a35daf79127c57256ecb",
        ),
        (
            99999999999,
            "test_memo",
            DESTINATION_ADDRESS,
            TRON_TEST_WALLET_PRIVATE_KEY,
            CreateTransactionError,
            "",
        ),
        (1, "test_memo", "d", TRON_TEST_WALLET_PRIVATE_KEY, CreateTransactionError, ""),
        (
            2,
            "test_memo",
            "Yge3Gid6vVaQvnPVRJ6SVwzC64cw2eBkN",
            TRON_TEST_WALLET_PRIVATE_KEY,
            CreateTransactionError,
            "",
        ),
        (1, "test_memo", DESTINATION_ADDRESS, "d", ValueError, ""),
    ],
)
@vcr_c.use_cassette("tron/send_trx.yaml")
async def test_send_trx(
    tron_client: AioTxTRONClient,
    amount,
    memo,
    send_to,
    private_key,
    expected_exception,
    expected_tx_id,
):
    sun_amount = tron_client.to_sun(amount)
    if expected_exception:
        with pytest.raises(expected_exception):
            await tron_client.send(private_key, send_to, sun_amount, memo)
    else:
        tx_id = await tron_client.send(private_key, send_to, sun_amount, memo)
        assert tx_id == expected_tx_id


@pytest.mark.parametrize(
    "amount, memo, send_to, contract, private_key, expected_exception, expected_tx_id",
    [
        (
            1,
            "",
            DESTINATION_ADDRESS,
            CONTRACT,
            TRON_TEST_WALLET_PRIVATE_KEY,
            None,
            "99dce8bfadc68a0388d7ff28702648402d4fe3dd50e916665368c0a0b6a28273",
        ),
        (
            1,
            5,
            DESTINATION_ADDRESS,
            CONTRACT,
            TRON_TEST_WALLET_PRIVATE_KEY,
            TypeError,
            "",
        ),
        (
            5,
            "orp3uhg$£(TUP42t38P(HU$h3r5g8))",
            DESTINATION_ADDRESS,
            CONTRACT,
            TRON_TEST_WALLET_PRIVATE_KEY,
            None,
            "f610753e84a5fe9b8fe72e1ac3175d5584887844e87f14cb08d532d0c66ff1ed",
        ),
        (
            99999999999,
            "test_memo",
            DESTINATION_ADDRESS,
            CONTRACT,
            TRON_TEST_WALLET_PRIVATE_KEY,
            None,
            "31dc98c67bdf5d21bda64f4c11c9fc3c629d3ea0dc437314615c852a27f09b8e",
        ),
        (1, "test_memo", "d", CONTRACT, TRON_TEST_WALLET_PRIVATE_KEY, TypeError, ""),
        (
            2,
            "test_memo",
            "Yge3Gid6vVaQvnPVRJ6SVwzC64cw2eBkN",
            CONTRACT,
            TRON_TEST_WALLET_PRIVATE_KEY,
            TypeError,
            "",
        ),
        (1, "test_memo", DESTINATION_ADDRESS, CONTRACT, "d", ValueError, ""),
        (
            99999999999,
            "",
            DESTINATION_ADDRESS,
            CONTRACT,
            TRON_TEST_WALLET_PRIVATE_KEY,
            None,
            "ff0c8255eda1cf21d3e3f150570e1798a7c0a320490b00623601ace17a769bb2",
        ),
        (
            1,
            "",
            DESTINATION_ADDRESS,
            "",
            TRON_TEST_WALLET_PRIVATE_KEY,
            CreateTransactionError,
            "53a4f1ef3614b49c530708c109556246bc87faab6d34a428e77c0419ea940041",
        ),
        (
            1,
            "",
            DESTINATION_ADDRESS,
            "d",
            TRON_TEST_WALLET_PRIVATE_KEY,
            CreateTransactionError,
            "53a4f1ef3614b49c530708c109556246bc87faab6d34a428e77c0419ea940041",
        ),
    ],
)
@vcr_c.use_cassette("tron/test_send_trc20_token.yaml")
async def test_send_trc20_token(
    tron_client: AioTxTRONClient,
    amount,
    memo,
    send_to,
    contract,
    private_key,
    expected_exception,
    expected_tx_id,
):
    # Because token is having 6 decimals too as TRX but check you token!
    sun_amount = tron_client.to_sun(amount)
    if expected_exception:
        with pytest.raises(expected_exception):
            await tron_client.send_token(
                private_key, send_to, contract, sun_amount, memo
            )
    else:
        tx_id = await tron_client.send_token(
            private_key, send_to, contract, sun_amount, memo
        )
        assert tx_id == expected_tx_id
