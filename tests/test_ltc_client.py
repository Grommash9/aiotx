from conftest import vcr_c
import os
from aiotx.clients import AioTxLTCClient


TEST_LTC_WALLET_PRIVATE_KEY = os.getenv("TEST_LTC_WALLET_PRIVATE_KEY")
assert TEST_LTC_WALLET_PRIVATE_KEY is not None, "add TEST_LTC_WALLET_PRIVATE_KEY"
TEST_LTC_ADDRESS = "tltc1qswslzcdulvlk62gdrg8wa0sw36f938h2cvtaf7"

@vcr_c.use_cassette("ltc/get_last_block.yaml")
async def test_get_last_block(ltc_public_client: AioTxLTCClient):
    block_id = await ltc_public_client.get_last_block_number()
    assert isinstance(block_id, int)


@vcr_c.use_cassette("ltc/get_block_by_number.yaml")
async def test_get_block_by_number(ltc_public_client: AioTxLTCClient):
    block = await ltc_public_client.get_block_by_number(3247846)
    assert isinstance(block, dict)

    assert block["hash"] == "4314081d2a5d8633c51799113aac1516f174d5da5793c966848ac34177fb61c9"

    tx_hashes = [tx["hash"] for tx in block["tx"]]
    assert "68e73174f7b44edad7289a771d3069ff91c8bbb30cf96ea9861a4a312c1a2dda" in tx_hashes
    assert "4676f0e42c940f827c7f3b580119c10fe282b39bdbb798dc96d9292c387b37f0" in tx_hashes




@vcr_c.use_cassette("ltc/send_transaction.yaml")
async def test_send_transaction(ltc_public_client: AioTxLTCClient):
    await ltc_public_client.monitor._add_new_address("tltc1q24gng65qj3wr55878324w2eeeta4k2plfwaf54")
    await ltc_public_client.monitor._add_new_utxo(TEST_LTC_ADDRESS,
                                            "b6ea5514e75b003a965ed9b28502084ccc60890c6e076e676ebe0595f225b232", 150000000, 0)

    amount = ltc_public_client.to_satoshi(0.5)
    fee = ltc_public_client.to_satoshi(0.005)
    tx_id = await ltc_public_client.send(TEST_LTC_WALLET_PRIVATE_KEY,
                                        "tltc1q24gng65qj3wr55878324w2eeeta4k2plfwaf54", amount, fee)
    assert tx_id == "374bc22ae7ee399fc9ea051651d68a6378c23b0da605112ba2119bb5d4e7c6cb"
    await ltc_public_client.monitor._delete_utxo("b6ea5514e75b003a965ed9b28502084ccc60890c6e076e676ebe0595f225b232", 0)

    


@vcr_c.use_cassette("ltc/send_bulk.yaml")
async def test_bulk_send_transaction(ltc_public_client: AioTxLTCClient):
    fee = ltc_public_client.to_satoshi(0.005)
    await ltc_public_client.monitor._add_new_address("tltc1q24gng65qj3wr55878324w2eeeta4k2plfwaf54")
    await ltc_public_client.monitor._add_new_utxo(TEST_LTC_ADDRESS,
                                            "374bc22ae7ee399fc9ea051651d68a6378c23b0da605112ba2119bb5d4e7c6cb", 99500000, 1)
    
    amount = ltc_public_client.to_satoshi(0.3)
    tx_id = await ltc_public_client.send_bulk(TEST_LTC_WALLET_PRIVATE_KEY,
                                        {"tltc1q24gng65qj3wr55878324w2eeeta4k2plfwaf54": amount,
                                         TEST_LTC_ADDRESS: amount}, fee)
    
    assert tx_id == "55863cc61de0c6c1c87282d3d6fb03650c0fc90ed3282191c618069cbde1d525"


@vcr_c.use_cassette("ltc/send_from_two_utxo.yaml")
async def test_send_from_two_utxo(ltc_public_client: AioTxLTCClient):
    fee = ltc_public_client.to_satoshi(0.005)
    await ltc_public_client.monitor._add_new_address("tltc1q24gng65qj3wr55878324w2eeeta4k2plfwaf54")
    await ltc_public_client.monitor._add_new_utxo(TEST_LTC_ADDRESS,
                                            "55863cc61de0c6c1c87282d3d6fb03650c0fc90ed3282191c618069cbde1d525", 39000000, 0)
    await ltc_public_client.monitor._add_new_utxo(TEST_LTC_ADDRESS,
                                            "55863cc61de0c6c1c87282d3d6fb03650c0fc90ed3282191c618069cbde1d525", 30000000, 2)
    
    amount = ltc_public_client.to_satoshi(0.66)
    tx_id = await ltc_public_client.send(TEST_LTC_WALLET_PRIVATE_KEY, TEST_LTC_ADDRESS, amount, fee)
    print("tx_id", tx_id)


