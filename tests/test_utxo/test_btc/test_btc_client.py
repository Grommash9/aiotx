import os
import sys

import pytest
from conftest import vcr_c

from aiotx.clients import AioTxBTCClient

TEST_BTC_WALLET_PRIVATE_KEY = os.getenv("TEST_BTC_WALLET_PRIVATE_KEY")
assert TEST_BTC_WALLET_PRIVATE_KEY is not None, "add TEST_BTC_WALLET_PRIVATE_KEY"
TEST_BTC_ADDRESS = "tb1qswslzcdulvlk62gdrg8wa0sw36f938h2pyfreh"

@pytest.mark.skipif(sys.platform == "win32", reason="Skipping transaction signing tests on Windows because we are not using RFC6979 from fastecdsa by default")
@vcr_c.use_cassette("btc/send_transaction.yaml")
async def test_send_transaction(btc_client: AioTxBTCClient):
    await btc_client.monitor._add_new_address(TEST_BTC_ADDRESS)
    await btc_client.monitor._add_new_utxo(TEST_BTC_ADDRESS,
                                            "25d56f693d5c4d00d3f98e58c8bd66e8db930e38c8a556bd67737b66cbf31ab9", 16263, 0)

    amount = 1000
    fee = btc_client.to_satoshi(0.00001)
    tx_id = await btc_client.send(TEST_BTC_WALLET_PRIVATE_KEY,
                                        "tb1q4tf08gc2vf8dgfqtd3jen3s5tddz6uu0mnyf90", amount, fee)
    assert tx_id == "4f9a64d28ae22134379f7da50282d7ca2ead8a1f8378b20e25defcaaa5c59228"
    await btc_client.monitor._delete_utxo("25d56f693d5c4d00d3f98e58c8bd66e8db930e38c8a556bd67737b66cbf31ab9", 0)


@pytest.mark.skipif(sys.platform == "win32", reason="Skipping transaction signing tests on Windows because we are not using RFC6979 from fastecdsa by default")
@vcr_c.use_cassette("btc/send_to_all_address_types.yaml")
async def test_send_to_all_address_types(btc_client: AioTxBTCClient):
    fee = btc_client.to_satoshi(0.00006)
    await btc_client.monitor._add_new_address(TEST_BTC_ADDRESS)
    await btc_client.monitor._add_new_utxo(TEST_BTC_ADDRESS,
                                            "25d56f693d5c4d00d3f98e58c8bd66e8db930e38c8a556bd67737b66cbf31ab9", 16263, 0)
    amount = 1000
    tx_id = await btc_client.send_bulk(TEST_BTC_WALLET_PRIVATE_KEY, {
        "mtkbaiLiUH3fvGJeSzuN3kUgmJzqinLejJ": amount,  # Legacy P2PKH address
        "2NDYhjHKdPLYjD5kVZVgeo8JxDrDUcRC14Q": amount,  # P2SH address
        "tb1qq4ay9zw2mygwucz47v6hsda04a9l2yajyynh00": amount,  # Bech32 address
        "tb1pwgjc67568cu6vncgve60t6eaht0rwr4pwdymnrpezrpepg3q5t8sp5250h": amount, # Bech32M address
    }, fee)
    assert tx_id == "35158b7a8b6057bc67f6d904c64b5986adea8260f0bc96cbd755b530878e3cc2"