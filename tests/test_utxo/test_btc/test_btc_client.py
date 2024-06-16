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
    utxo_list = await btc_client.monitor._get_utxo_data(TEST_BTC_ADDRESS)
    assert len(utxo_list) == 1
    assert (
        utxo_list[0][0]
        == "4f9a64d28ae22134379f7da50282d7ca2ead8a1f8378b20e25defcaaa5c59228"
    )
    assert utxo_list[0][2] == 14263
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
        utxo_list[0][0]
        == "35158b7a8b6057bc67f6d904c64b5986adea8260f0bc96cbd755b530878e3cc2"
    )
    assert utxo_list[0][2] == 6263
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


# @pytest.mark.skipif(
#     sys.platform == "win32",
#     reason="Skipping transaction signing tests on Windows because we are not using RFC6979 from fastecdsa by default",
# )
# @vcr_c.use_cassette("btc/cpfp_transaction.yaml")
# async def test_cpfp_transaction(btc_client: AioTxBTCClient):
#     amount = btc_client.to_satoshi(3.68059994)
#     await btc_client.monitor._add_new_address(TEST_BTC_ADDRESS)
#     await btc_client.monitor._add_new_utxo(
#         TEST_BTC_ADDRESS,
#         "dea64fb299ea06975a74d460c1515c689df40d4878f0579af9b20cb987032e62",
#         amount,
#         0,
#     )

#     amount = 1000

#     tx_id = await btc_client.send(
#         TEST_BTC_WALLET_PRIVATE_KEY,
#         "tb1p2tzs7ghuanrm8mmqqjgvm2fdkkl4t6yvmupmt8wwpvsgwcj2vsasvwnjvy",
#         amount,
#         total_fee=200,
#     )


#     utxo_list = await btc_client.monitor._get_utxo_data(TEST_BTC_ADDRESS)
#     assert len(utxo_list) == 1
#     assert (
#         utxo_list[0][0]
#         == "4f9a64d28ae22134379f7da50282d7ca2ead8a1f8378b20e25defcaaa5c59228"
#     )
#     assert utxo_list[0][2] == 14263
#     assert tx_id == "4f9a64d28ae22134379f7da50282d7ca2ead8a1f8378b20e25defcaaa5c59228"
#     await btc_client.monitor._delete_utxo(
#         "25d56f693d5c4d00d3f98e58c8bd66e8db930e38c8a556bd67737b66cbf31ab9", 0
#     )
