import os

from conftest import vcr_c

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
    await ltc_public_client.monitor._add_new_address(TEST_LTC_ADDRESS)
    await ltc_public_client.monitor._add_new_utxo(TEST_LTC_ADDRESS,
                                            "55863cc61de0c6c1c87282d3d6fb03650c0fc90ed3282191c618069cbde1d525", 39000000, 0)

    amount = ltc_public_client.to_satoshi(0.1)
    fee = ltc_public_client.to_satoshi(0.005)
    tx_id = await ltc_public_client.send(TEST_LTC_WALLET_PRIVATE_KEY,
                                        "tltc1q24gng65qj3wr55878324w2eeeta4k2plfwaf54", amount, fee)
    assert tx_id == "a006aedf3a08f423434aa781988997a0526f9365fe228fb8934ea64bbbb9d055"
    await ltc_public_client.monitor._delete_utxo("55863cc61de0c6c1c87282d3d6fb03650c0fc90ed3282191c618069cbde1d525", 0)

    


@vcr_c.use_cassette("ltc/send_bulk.yaml")
async def test_bulk_send_transaction(ltc_public_client: AioTxLTCClient):
    fee = ltc_public_client.to_satoshi(0.005)
    await ltc_public_client.monitor._add_new_address(TEST_LTC_ADDRESS)
    await ltc_public_client.monitor._add_new_utxo(TEST_LTC_ADDRESS,
                                            "55863cc61de0c6c1c87282d3d6fb03650c0fc90ed3282191c618069cbde1d525", 30000000, 2)
    
    amount = ltc_public_client.to_satoshi(0.05) - fee / 2
    tx_id = await ltc_public_client.send_bulk(TEST_LTC_WALLET_PRIVATE_KEY,
                                        {"tltc1q24gng65qj3wr55878324w2eeeta4k2plfwaf54": amount,
                                         "tltc1qshy0jeejm4pw3ep4cedc5vlmxyz348epnk7etf": amount}, fee)
    
    assert tx_id == "64a89e7e269469c126e96d1de7b553850716c71d9081b153429ff781758a59a1"


@vcr_c.use_cassette("ltc/send_from_two_utxo.yaml")
async def test_send_from_two_utxo(ltc_public_client: AioTxLTCClient):
    fee = ltc_public_client.to_satoshi(0.005)
    await ltc_public_client.monitor._add_new_address(TEST_LTC_ADDRESS)
    await ltc_public_client.monitor._add_new_utxo(TEST_LTC_ADDRESS,
                                            "a006aedf3a08f423434aa781988997a0526f9365fe228fb8934ea64bbbb9d055", 28500000, 0)
    await ltc_public_client.monitor._add_new_utxo(TEST_LTC_ADDRESS,
                                            "64a89e7e269469c126e96d1de7b553850716c71d9081b153429ff781758a59a1", 20000000, 0)
    amount = 28500000 + 20000000 - fee
    tx_id = await ltc_public_client.send(TEST_LTC_WALLET_PRIVATE_KEY, TEST_LTC_ADDRESS, amount, fee)
    assert tx_id == "3fcd11698664ffea5fe00adef6bd2c1c35de66c3fafb50f9076c74ff13fea139"


@vcr_c.use_cassette("ltc/send_to_legacy_address.yaml")
async def test_send_to_legacy_address(ltc_public_client: AioTxLTCClient):
    fee = ltc_public_client.to_satoshi(0.005)
    await ltc_public_client.monitor._add_new_address(TEST_LTC_ADDRESS)
    await ltc_public_client.monitor._add_new_utxo(TEST_LTC_ADDRESS,
                                            "3fcd11698664ffea5fe00adef6bd2c1c35de66c3fafb50f9076c74ff13fea139", 48000000, 0)
    amount = ltc_public_client.to_satoshi(0.005)
    tx_id = await ltc_public_client.send(TEST_LTC_WALLET_PRIVATE_KEY, "mq2PZs9p5ZNLbu23KLKb1tdQt1mrBJM7CX", amount, fee)
    assert tx_id == "141c30ea6326ab447423465d2a7f4c3067812f06ef1e505c0443e85c06ed684a"


@vcr_c.use_cassette("ltc/send_to_legacy_and_segwit_addresses.yaml")
async def test_send_to_legacy_and_segwit_address(ltc_public_client: AioTxLTCClient):
    fee = ltc_public_client.to_satoshi(0.005)
    await ltc_public_client.monitor._add_new_address(TEST_LTC_ADDRESS)
    await ltc_public_client.monitor._add_new_utxo(TEST_LTC_ADDRESS,
                                            "141c30ea6326ab447423465d2a7f4c3067812f06ef1e505c0443e85c06ed684a", 47000000, 0)
    amount = ltc_public_client.to_satoshi(0.005)
    tx_id = await ltc_public_client.send_bulk(TEST_LTC_WALLET_PRIVATE_KEY, {"mq2PZs9p5ZNLbu23KLKb1tdQt1mrBJM7CX": amount,
                                                                            "tltc1q24gng65qj3wr55878324w2eeeta4k2plfwaf54": amount}, fee)
    assert tx_id == "33f67e7ac0dde523598f416f8efa5928d9e8a4a681db48f7df7d174701225dd0"