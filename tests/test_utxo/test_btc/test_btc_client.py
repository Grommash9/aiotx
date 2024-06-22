import os
import sys

import pytest
from conftest import vcr_c

from aiotx.clients import AioTxBTCClient
from aiotx.exceptions import NotImplementedError, RpcConnectionError
from aiotx.types import FeeEstimate

TEST_BTC_WALLET_PRIVATE_KEY = os.getenv("TEST_BTC_WALLET_PRIVATE_KEY")
assert TEST_BTC_WALLET_PRIVATE_KEY is not None, "add TEST_BTC_WALLET_PRIVATE_KEY"
TEST_BTC_ADDRESS = "tb1qswslzcdulvlk62gdrg8wa0sw36f938h2pyfreh"


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Skipping transaction signing tests on Windows because we are not using RFC6979 from fastecdsa by default",
)
@vcr_c.use_cassette("btc/send_transaction.yaml")
async def test_send_transaction(btc_client: AioTxBTCClient):
    await btc_client.monitor._add_new_address(TEST_BTC_ADDRESS)
    await btc_client.monitor._add_new_utxo(
        TEST_BTC_ADDRESS,
        "25d56f693d5c4d00d3f98e58c8bd66e8db930e38c8a556bd67737b66cbf31ab9",
        16263,
        0,
    )

    amount = 1000
    fee = btc_client.to_satoshi(0.00001)
    tx_id = await btc_client.send(
        TEST_BTC_WALLET_PRIVATE_KEY,
        "tb1q4tf08gc2vf8dgfqtd3jen3s5tddz6uu0mnyf90",
        amount,
        fee,
    )
    utxo_list = await btc_client.monitor._get_utxo_data(TEST_BTC_ADDRESS)
    assert len(utxo_list) == 1
    assert (
        utxo_list[0].tx_id
        == "4f9a64d28ae22134379f7da50282d7ca2ead8a1f8378b20e25defcaaa5c59228"
    )
    assert utxo_list[0].amount_satoshi == 14263
    assert tx_id == "4f9a64d28ae22134379f7da50282d7ca2ead8a1f8378b20e25defcaaa5c59228"
    await btc_client.monitor._delete_utxo(
        "25d56f693d5c4d00d3f98e58c8bd66e8db930e38c8a556bd67737b66cbf31ab9", 0
    )


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Skipping transaction signing tests on Windows because we are not using RFC6979 from fastecdsa by default",
)
@vcr_c.use_cassette("btc/send_to_all_address_types.yaml")
async def test_send_to_all_address_types(btc_client: AioTxBTCClient):
    fee = btc_client.to_satoshi(0.00006)
    await btc_client.monitor._add_new_address(TEST_BTC_ADDRESS)
    await btc_client.monitor._add_new_utxo(
        TEST_BTC_ADDRESS,
        "25d56f693d5c4d00d3f98e58c8bd66e8db930e38c8a556bd67737b66cbf31ab9",
        16263,
        0,
    )
    amount = 1000
    tx_id = await btc_client.send_bulk(
        TEST_BTC_WALLET_PRIVATE_KEY,
        {
            "mtkbaiLiUH3fvGJeSzuN3kUgmJzqinLejJ": amount,  # Legacy P2PKH address
            "2NDYhjHKdPLYjD5kVZVgeo8JxDrDUcRC14Q": amount,  # P2SH address
            "tb1qq4ay9zw2mygwucz47v6hsda04a9l2yajyynh00": amount,  # Bech32 address
            "tb1pwgjc67568cu6vncgve60t6eaht0rwr4pwdymnrpezrpepg3q5t8sp5250h": amount,  # Bech32M address
        },
        fee,
    )
    utxo_list = await btc_client.monitor._get_utxo_data(TEST_BTC_ADDRESS)
    assert len(utxo_list) == 1
    assert (
        utxo_list[0].tx_id
        == "35158b7a8b6057bc67f6d904c64b5986adea8260f0bc96cbd755b530878e3cc2"
    )
    assert utxo_list[0].amount_satoshi == 6263
    assert tx_id == "35158b7a8b6057bc67f6d904c64b5986adea8260f0bc96cbd755b530878e3cc2"


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Skipping transaction signing tests on Windows because we are not using RFC6979 from fastecdsa by default",
)
@vcr_c.use_cassette("btc/send_with_auto_fee.yaml")
async def test_send_with_auto_fee(btc_client: AioTxBTCClient):
    await btc_client.monitor._add_new_address(TEST_BTC_ADDRESS)
    await btc_client.monitor._add_new_utxo(
        TEST_BTC_ADDRESS,
        " 35158b7a8b6057bc67f6d904c64b5986adea8260f0bc96cbd755b530878e3cc2 ",
        6263,
        0,
    )
    amount = 1000
    tx_id = await btc_client.send_bulk(
        TEST_BTC_WALLET_PRIVATE_KEY,
        {"mtkbaiLiUH3fvGJeSzuN3kUgmJzqinLejJ": amount},
        conf_target=1,
        estimate_mode=FeeEstimate.CONSERVATIVE,
    )

    assert tx_id == "77cb20c4b0325242b9e5f45f4850e5387dc585d6b72bb36ba65a126534436973"

    utxo_list = await btc_client.monitor._get_utxo_data(TEST_BTC_ADDRESS)
    assert len(utxo_list) == 0


@vcr_c.use_cassette("btc/test_get_balance.yaml")
async def test_get_balance(btc_client: AioTxBTCClient):
    await btc_client.monitor._add_new_address(TEST_BTC_ADDRESS)
    await btc_client.monitor._add_new_utxo(
        TEST_BTC_ADDRESS,
        "35158b7a8b6057bc67f6d904c64b5986adea8260f0bc96cbd755b530878e3cc2 ",
        6263,
        0,
    )

    balance = await btc_client.get_balance(TEST_BTC_ADDRESS)
    assert balance == 6263

    await btc_client.monitor._delete_utxo(
        "35158b7a8b6057bc67f6d904c64b5986adea8260f0bc96cbd755b530878e3cc2 ", 0
    )

    balance = await btc_client.get_balance(TEST_BTC_ADDRESS)
    assert balance == 0

    await btc_client.monitor._add_new_utxo(
        TEST_BTC_ADDRESS,
        "35158b7a8b6057bc67f6d904c64b5986adea8260f0bc96cbd755b530878e3cc2 ",
        6263,
        0,
    )
    balance = await btc_client.get_balance(TEST_BTC_ADDRESS)
    assert balance == 6263

    await btc_client.monitor._mark_utxo_used(
        "35158b7a8b6057bc67f6d904c64b5986adea8260f0bc96cbd755b530878e3cc2 ", 0
    )

    balance = await btc_client.get_balance(TEST_BTC_ADDRESS)
    assert balance == 0


@pytest.mark.mysql
@vcr_c.use_cassette("btc/test_get_balance_mysql.yaml")
async def test_get_balance_mysql(btc_client_mysql: AioTxBTCClient):
    await btc_client_mysql.monitor._add_new_address(TEST_BTC_ADDRESS)
    await btc_client_mysql.monitor._add_new_utxo(
        TEST_BTC_ADDRESS,
        "35158b7a8b6057bc67f6d904c64b5986adea8260f0bc96cbd755b530878e3cc2 ",
        6263,
        0,
    )

    balance = await btc_client_mysql.get_balance(TEST_BTC_ADDRESS)
    assert balance == 6263

    await btc_client_mysql.monitor._delete_utxo(
        "35158b7a8b6057bc67f6d904c64b5986adea8260f0bc96cbd755b530878e3cc2 ", 0
    )

    balance = await btc_client_mysql.get_balance(TEST_BTC_ADDRESS)
    assert balance == 0

    await btc_client_mysql.monitor._add_new_utxo(
        TEST_BTC_ADDRESS,
        "35158b7a8b6057bc67f6d904c64b5986adea8260f0bc96cbd755b530878e3cc2 ",
        6263,
        0,
    )
    balance = await btc_client_mysql.get_balance(TEST_BTC_ADDRESS)
    assert balance == 6263

    await btc_client_mysql.monitor._mark_utxo_used(
        "35158b7a8b6057bc67f6d904c64b5986adea8260f0bc96cbd755b530878e3cc2 ", 0
    )

    balance = await btc_client_mysql.get_balance(TEST_BTC_ADDRESS)
    assert balance == 0


@pytest.mark.parametrize(
    "tx_id, expected_exception, expected_fee",
    [
        (
            "35158b7a8b6057bc67f6d904c64b5986adea8260f0bc96cbd755b530878e3cc2",
            None,
            6000,
        ),
        (
            "77cb20c4b0325242b9e5f45f4850e5387dc585d6b72bb36ba65a126534436973",
            None,
            5263,
        ),
        (
            "25d56f693d5c4d00d3f98e58c8bd66e8db930e38c8a556bd67737b66cbf31ab9",
            None,
            6890,
        ),
        (
            "12d9d269b4468aaf663b0712e9cef2b1a86fc7e758094af19434b0de86208611",
            None,
            648000,
        ),
        (
            "07ce6824d6c7ee226c3d311d6729d06144b0cb1fd371208b7466a6283de0c2fe",
            None,
            462000,
        ),
        (
            "2ab5a6a291ece2240642369589442029a6ae4baaefb83ff6760893e542f2f8ac",
            NotImplementedError,
            0,
        ),
        (
            "55863cc61de0c6c1c87282d3d6fb03650c0fc90ed3282191c618069cbde1d5",
            RpcConnectionError,
            0,
        ),
        (
            "863cc61de0c6c1c87282d3d6fb03650c0fc90ed3282191c618069cbde1d525",
            RpcConnectionError,
            0,
        ),
    ],
)
@vcr_c.use_cassette("btc/get_tx_fee.yaml")
async def test_get_tx_fee(
    btc_client: AioTxBTCClient, tx_id, expected_exception, expected_fee
):
    if expected_exception:
        with pytest.raises(expected_exception):
            await btc_client.get_tx_fee(tx_id)
    else:
        fee = await btc_client.get_tx_fee(tx_id)
        assert isinstance(fee, int)
        assert fee == expected_fee


@pytest.mark.parametrize(
    "tx_id, expected_exception",
    [
        (
            "35158b7a8b6057bc67f6d904c64b5986adea8260f0bc96cbd755b530878e3cc2",
            None,
        ),
        (
            "77cb20c4b0325242b9e5f45f4850e5387dc585d6b72bb36ba65a126534436973",
            None,
        ),
        (
            "2ab5a6a291ece2240642369589442029a6ae4baaefb83ff6760893e542f2f8ac",
            None,
        ),
        (
            "55863cc61de0c6c1c87282d3d6fb03650c0fc90ed3282191c618069cbde1d5",
            RpcConnectionError,
        ),
        (
            "863cc61de0c6c1c87282d3d6fb03650c0fc90ed3282191c618069cbde1d525",
            RpcConnectionError,
        ),
    ],
)
@vcr_c.use_cassette("btc/get_raw_transaction.yaml")
async def test_get_raw_transaction(
    btc_client: AioTxBTCClient, tx_id, expected_exception
):
    if expected_exception:
        with pytest.raises(expected_exception):
            await btc_client.get_raw_transaction(tx_id)
    else:
        tx_data = await btc_client.get_raw_transaction(tx_id)
        assert isinstance(tx_data, dict)
        assert "txid" in tx_data.keys()


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Skipping transaction signing tests on Windows because we are not using RFC6979 from fastecdsa by default",
)
@vcr_c.use_cassette("btc/speed_up_transaction.yaml")
async def test_speed_up_transaction(btc_client: AioTxBTCClient):
    amount = btc_client.to_satoshi(3.6473502)
    await btc_client.monitor._add_new_address(TEST_BTC_ADDRESS)
    await btc_client.monitor._add_new_utxo(
        TEST_BTC_ADDRESS,
        "9e6fd5e4c946bde7f96c7f5921c46588f2462c33d68315b266373bf60735a39e",
        amount,
        0,
    )
    amount = 1000

    parent_tx_id = await btc_client.send(
        TEST_BTC_WALLET_PRIVATE_KEY,
        "tb1p2tzs7ghuanrm8mmqqjgvm2fdkkl4t6yvmupmt8wwpvsgwcj2vsasvwnjvy",
        amount,
        total_fee=int(btc_client.to_satoshi(0.00154914) / 6),
    )

    assert (
        parent_tx_id
        == "83d4a70c215017ae757b504c1c9f076b7dad31544d994b862113466d12318c48"
    )

    child_tx_id = await btc_client.speed_up_transaction_by_self_child_payment(
        TEST_BTC_WALLET_PRIVATE_KEY,
        "83d4a70c215017ae757b504c1c9f076b7dad31544d994b862113466d12318c48",
        conf_target=1,
    )
    assert (
        child_tx_id
        == "30aebb6b7f1b80ffd8700fb492e1a2820b8a04e7d6c95ddb8a163c138f6690b4"
    )


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Skipping transaction signing tests on Windows because we are not using RFC6979 from fastecdsa by default",
)
@vcr_c.use_cassette("btc/speed_up_transaction_not_enough_outputs.yaml")
async def test_speed_up_transaction_not_enough_outputs(btc_client: AioTxBTCClient):
    await btc_client.monitor._add_new_address(TEST_BTC_ADDRESS)

    await btc_client.monitor._add_new_utxo(
        TEST_BTC_ADDRESS,
        "b68f08d7e9e98c48460475eebd820dddc956f87857f573770f20aa67e70e8df9",
        btc_client.to_satoshi(0.0006635),
        1,
    )

    amount = 500
    parent_tx_id = await btc_client.send(
        TEST_BTC_WALLET_PRIVATE_KEY,
        TEST_BTC_ADDRESS,
        amount,
        total_fee=btc_client.to_satoshi(0.0006635) - amount,
    )

    assert (
        parent_tx_id
        == "371e7db7f99ca03cdcd96c69e2822ed3c384f418f7239b388c3ad9e63adfd76f"
    )

    await btc_client.monitor._add_new_utxo(
        TEST_BTC_ADDRESS,
        "b68f08d7e9e98c48460475eebd820dddc956f87857f573770f20aa67e70e8df9",
        btc_client.to_satoshi(3.65162827),
        0,
    )

    child_tx_id = await btc_client.speed_up_transaction_by_self_child_payment(
        TEST_BTC_WALLET_PRIVATE_KEY,
        "48b4c17afda93204f0875987a9281b4bfd90c29a5590046f09a5e3d910fab8f2",
        conf_target=1,
    )
    assert (
        child_tx_id
        == "9e6fd5e4c946bde7f96c7f5921c46588f2462c33d68315b266373bf60735a39e"
    )


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Skipping transaction signing tests on Windows because we are not using RFC6979 from fastecdsa by default",
)
@vcr_c.use_cassette("btc/bulk_send.yaml")
async def test_bulk_send(btc_client: AioTxBTCClient):
    await btc_client.monitor._add_new_address(TEST_BTC_ADDRESS)

    await btc_client.monitor._add_new_utxo(
        TEST_BTC_ADDRESS,
        "a7d8e3dea2da06c30dde62f3ead03b9260372e09b77fd74aebc7d58245a4a8bc",
        btc_client.to_satoshi(3.65416086),
        0,
    )

    tx_id = await btc_client.send_bulk(
        TEST_BTC_WALLET_PRIVATE_KEY,
        destinations={
            TEST_BTC_ADDRESS: btc_client.to_satoshi(0.0006635),
            "tb1p2tzs7ghuanrm8mmqqjgvm2fdkkl4t6yvmupmt8wwpvsgwcj2vsasvwnjvy": 600,
        },
    )
    assert tx_id == "b68f08d7e9e98c48460475eebd820dddc956f87857f573770f20aa67e70e8df9"
