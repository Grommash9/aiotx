import os
import sys

import pytest
from conftest import vcr_c

from aiotx.clients import AioTxBTCClient

TEST_BTC_WALLET_PRIVATE_KEY = os.getenv("TEST_BTC_WALLET_PRIVATE_KEY")
assert TEST_BTC_WALLET_PRIVATE_KEY is not None, "add TEST_BTC_WALLET_PRIVATE_KEY"
TEST_BTC_ADDRESS = "tb1qswslzcdulvlk62gdrg8wa0sw36f938h2pyfreh"

@pytest.mark.skipif(sys.platform == "win32", reason="Skipping transaction signing tests on Windows")
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


# @vcr_c.use_cassette("ltc/send_bulk_legacy_and_segwit_tx.yaml")
# async def test_bulk_send_transaction(btc_client: AioTxBTCClient):
#     fee = btc_client.to_satoshi(0.00001)
#     await btc_client.monitor._add_new_address(TEST_BTC_ADDRESS)
#     await btc_client.monitor._add_new_utxo(TEST_BTC_ADDRESS,
#                                             "4f9a64d28ae22134379f7da50282d7ca2ead8a1f8378b20e25defcaaa5c59228", 14263, 0)
    
#     amount = 1000 - fee / 2
#     tx_id = await btc_client.send_bulk(TEST_BTC_WALLET_PRIVATE_KEY,
#                                         {"tltc1q24gng65qj3wr55878324w2eeeta4k2plfwaf54": amount,
#                                          "2N5GkkPqPNYVVRibjxPBpPgAPoxfVh16eax": amount,
#                                          TEST_BTC_ADDRESS: amount}, fee)
    
#     assert tx_id == "64a89e7e269469c126e96d1de7b553850716c71d9081b153429ff781758a59a1"