import asyncio
import os
import sys

import pytest
from conftest import vcr_c

from aiotx.clients import AioTxLTCClient
from aiotx.exceptions import InsufficientFunds, NotImplementedError, RpcConnectionError

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

    assert (
        block["hash"]
        == "4314081d2a5d8633c51799113aac1516f174d5da5793c966848ac34177fb61c9"
    )

    tx_hashes = [tx["hash"] for tx in block["tx"]]
    assert (
        "68e73174f7b44edad7289a771d3069ff91c8bbb30cf96ea9861a4a312c1a2dda" in tx_hashes
    )
    assert (
        "4676f0e42c940f827c7f3b580119c10fe282b39bdbb798dc96d9292c387b37f0" in tx_hashes
    )


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Skipping transaction signing tests on Windows because we are not using RFC6979 from fastecdsa by default",
)
@vcr_c.use_cassette("ltc/send_transaction.yaml")
async def test_send_transaction(ltc_public_client: AioTxLTCClient):
    await ltc_public_client.monitor._add_new_address(TEST_LTC_ADDRESS)
    await ltc_public_client.monitor._add_new_utxo(
        TEST_LTC_ADDRESS,
        "55863cc61de0c6c1c87282d3d6fb03650c0fc90ed3282191c618069cbde1d525",
        39000000,
        0,
    )

    amount = ltc_public_client.to_satoshi(0.1)
    fee = ltc_public_client.to_satoshi(0.005)
    tx_id = await ltc_public_client.send(
        TEST_LTC_WALLET_PRIVATE_KEY,
        "tltc1q24gng65qj3wr55878324w2eeeta4k2plfwaf54",
        amount,
        fee,
    )
    assert tx_id == "a006aedf3a08f423434aa781988997a0526f9365fe228fb8934ea64bbbb9d055"
    utxo_list = await ltc_public_client.monitor._get_utxo_data(TEST_LTC_ADDRESS)
    assert len(utxo_list) == 1
    assert (
        utxo_list[0].tx_id
        == "a006aedf3a08f423434aa781988997a0526f9365fe228fb8934ea64bbbb9d055"
    )
    assert utxo_list[0].amount_satoshi == 28500000
    await ltc_public_client.monitor._delete_utxo(
        "55863cc61de0c6c1c87282d3d6fb03650c0fc90ed3282191c618069cbde1d525", 0
    )


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Skipping transaction signing tests on Windows because we are not using RFC6979 from fastecdsa by default",
)
@vcr_c.use_cassette("ltc/send_bulk.yaml")
async def test_bulk_send_transaction(ltc_public_client: AioTxLTCClient):
    fee = ltc_public_client.to_satoshi(0.005)
    await ltc_public_client.monitor._add_new_address(TEST_LTC_ADDRESS)
    await ltc_public_client.monitor._add_new_utxo(
        TEST_LTC_ADDRESS,
        "55863cc61de0c6c1c87282d3d6fb03650c0fc90ed3282191c618069cbde1d525",
        30000000,
        2,
    )

    amount = ltc_public_client.to_satoshi(0.05) - fee / 2
    tx_id = await ltc_public_client.send_bulk(
        TEST_LTC_WALLET_PRIVATE_KEY,
        {
            "tltc1q24gng65qj3wr55878324w2eeeta4k2plfwaf54": amount,
            "tltc1qshy0jeejm4pw3ep4cedc5vlmxyz348epnk7etf": amount,
        },
        fee,
    )
    utxo_list = await ltc_public_client.monitor._get_utxo_data(TEST_LTC_ADDRESS)
    assert len(utxo_list) == 1
    assert (
        utxo_list[0].tx_id
        == "64a89e7e269469c126e96d1de7b553850716c71d9081b153429ff781758a59a1"
    )
    assert utxo_list[0].amount_satoshi == 20000000
    assert tx_id == "64a89e7e269469c126e96d1de7b553850716c71d9081b153429ff781758a59a1"


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Skipping transaction signing tests on Windows because we are not using RFC6979 from fastecdsa by default",
)
@vcr_c.use_cassette("ltc/send_from_two_utxo.yaml")
async def test_send_from_two_utxo(ltc_public_client: AioTxLTCClient):
    fee = ltc_public_client.to_satoshi(0.005)
    await ltc_public_client.monitor._add_new_address(TEST_LTC_ADDRESS)
    await ltc_public_client.monitor._add_new_utxo(
        TEST_LTC_ADDRESS,
        "a006aedf3a08f423434aa781988997a0526f9365fe228fb8934ea64bbbb9d055",
        28500000,
        0,
    )
    await ltc_public_client.monitor._add_new_utxo(
        TEST_LTC_ADDRESS,
        "64a89e7e269469c126e96d1de7b553850716c71d9081b153429ff781758a59a1",
        20000000,
        0,
    )
    amount = 28500000 + 20000000 - fee
    tx_id = await ltc_public_client.send(
        TEST_LTC_WALLET_PRIVATE_KEY, TEST_LTC_ADDRESS, amount, fee
    )
    utxo_list = await ltc_public_client.monitor._get_utxo_data(TEST_LTC_ADDRESS)
    assert len(utxo_list) == 1
    assert (
        utxo_list[0].tx_id
        == "3fcd11698664ffea5fe00adef6bd2c1c35de66c3fafb50f9076c74ff13fea139"
    )
    assert utxo_list[0].amount_satoshi == 48000000
    assert tx_id == "3fcd11698664ffea5fe00adef6bd2c1c35de66c3fafb50f9076c74ff13fea139"


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Skipping transaction signing tests on Windows because we are not using RFC6979 from fastecdsa by default",
)
@vcr_c.use_cassette("ltc/send_to_legacy_address.yaml")
async def test_send_to_legacy_address(ltc_public_client: AioTxLTCClient):
    fee = ltc_public_client.to_satoshi(0.005)
    await ltc_public_client.monitor._add_new_address(TEST_LTC_ADDRESS)
    await ltc_public_client.monitor._add_new_utxo(
        TEST_LTC_ADDRESS,
        "3fcd11698664ffea5fe00adef6bd2c1c35de66c3fafb50f9076c74ff13fea139",
        48000000,
        0,
    )
    amount = ltc_public_client.to_satoshi(0.005)
    tx_id = await ltc_public_client.send(
        TEST_LTC_WALLET_PRIVATE_KEY, "mq2PZs9p5ZNLbu23KLKb1tdQt1mrBJM7CX", amount, fee
    )
    utxo_list = await ltc_public_client.monitor._get_utxo_data(TEST_LTC_ADDRESS)
    assert len(utxo_list) == 1
    assert (
        utxo_list[0].tx_id
        == "141c30ea6326ab447423465d2a7f4c3067812f06ef1e505c0443e85c06ed684a"
    )
    assert utxo_list[0].amount_satoshi == 47000000
    assert tx_id == "141c30ea6326ab447423465d2a7f4c3067812f06ef1e505c0443e85c06ed684a"


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Skipping transaction signing tests on Windows because we are not using RFC6979 from fastecdsa by default",
)
@vcr_c.use_cassette("ltc/send_to_legacy_and_segwit_addresses.yaml")
async def test_send_to_legacy_and_segwit_address(ltc_public_client: AioTxLTCClient):
    fee = ltc_public_client.to_satoshi(0.005)
    await ltc_public_client.monitor._add_new_address(TEST_LTC_ADDRESS)
    await ltc_public_client.monitor._add_new_utxo(
        TEST_LTC_ADDRESS,
        "141c30ea6326ab447423465d2a7f4c3067812f06ef1e505c0443e85c06ed684a",
        47000000,
        0,
    )
    amount = ltc_public_client.to_satoshi(0.005)
    tx_id = await ltc_public_client.send_bulk(
        TEST_LTC_WALLET_PRIVATE_KEY,
        {
            "mq2PZs9p5ZNLbu23KLKb1tdQt1mrBJM7CX": amount,
            "tltc1q24gng65qj3wr55878324w2eeeta4k2plfwaf54": amount,
        },
        fee,
    )
    utxo_list = await ltc_public_client.monitor._get_utxo_data(TEST_LTC_ADDRESS)
    assert len(utxo_list) == 1
    assert (
        utxo_list[0].tx_id
        == "33f67e7ac0dde523598f416f8efa5928d9e8a4a681db48f7df7d174701225dd0"
    )
    assert utxo_list[0].amount_satoshi == 45500000
    assert tx_id == "33f67e7ac0dde523598f416f8efa5928d9e8a4a681db48f7df7d174701225dd0"


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Skipping transaction signing tests on Windows because we are not using RFC6979 from fastecdsa by default",
)
@vcr_c.use_cassette("ltc/send_with_auto_fee.yaml")
async def test_send_with_auto_fee(ltc_public_client: AioTxLTCClient):
    await ltc_public_client.monitor._add_new_address(TEST_LTC_ADDRESS)
    await ltc_public_client.monitor._add_new_utxo(
        TEST_LTC_ADDRESS,
        "33f67e7ac0dde523598f416f8efa5928d9e8a4a681db48f7df7d174701225dd0",
        45500000,
        0,
    )
    amount = ltc_public_client.to_satoshi(0.005)
    tx_id = await ltc_public_client.send(
        TEST_LTC_WALLET_PRIVATE_KEY, "mq2PZs9p5ZNLbu23KLKb1tdQt1mrBJM7CX", amount
    )
    utxo_list = await ltc_public_client.monitor._get_utxo_data(TEST_LTC_ADDRESS)
    assert len(utxo_list) == 1
    assert (
        utxo_list[0].tx_id
        == "ac3c62cb37887a41235fecbc8dd22c8a8b5b74e1d2695dbc78e6d05a0cbdf2e9"
    )
    assert utxo_list[0].amount_satoshi == 44999715
    assert tx_id == "ac3c62cb37887a41235fecbc8dd22c8a8b5b74e1d2695dbc78e6d05a0cbdf2e9"


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Skipping transaction signing tests on Windows because we are not using RFC6979 from fastecdsa by default",
)
@vcr_c.use_cassette("ltc/send_with_auto_fee_and_deduct_commission.yaml")
async def test_send_with_auto_fee_and_deduct_commission(
    ltc_public_client: AioTxLTCClient,
):
    await ltc_public_client.monitor._add_new_address(TEST_LTC_ADDRESS)
    utxo_amount = ltc_public_client.to_satoshi(0.44448584)
    await ltc_public_client.monitor._add_new_utxo(
        TEST_LTC_ADDRESS,
        "487933e5f8028e9235f76dacb368efd64bb6f038989ff92b217661c192f0055f",
        utxo_amount,
        0,
    )
    amount = ltc_public_client.to_satoshi(0.0055)
    tx_id = await ltc_public_client.send(
        TEST_LTC_WALLET_PRIVATE_KEY,
        "mq2PZs9p5ZNLbu23KLKb1tdQt1mrBJM7CX",
        amount,
        deduct_fee=True,
    )
    utxo_list = await ltc_public_client.monitor._get_utxo_data(TEST_LTC_ADDRESS)
    assert len(utxo_list) == 1
    assert (
        utxo_list[0].tx_id
        == "3ed6c7a8e3b263679c47223f3e9c65721f865378e1b6799182f0607e1ebf9179"
    )
    assert utxo_list[0].amount_satoshi == 43898584
    assert tx_id == "3ed6c7a8e3b263679c47223f3e9c65721f865378e1b6799182f0607e1ebf9179"


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Skipping transaction signing tests on Windows because we are not using RFC6979 from fastecdsa by default",
)
@vcr_c.use_cassette("ltc/bulk_send_with_auto_fee_and_deduct_commission.yaml")
async def test_bulk_send_with_auto_fee_and_deduct_commission(
    ltc_public_client: AioTxLTCClient,
):
    await ltc_public_client.monitor._add_new_address(TEST_LTC_ADDRESS)
    utxo_amount = ltc_public_client.to_satoshi(0.43397453)
    await ltc_public_client.monitor._add_new_utxo(
        TEST_LTC_ADDRESS,
        "3f7e5e1a897b6698d551f2b576d15eda85bf1c0d2706f7cb8c4b17a75632d1d2",
        utxo_amount,
        0,
    )
    amount = ltc_public_client.to_satoshi(0.005)
    tx_id = await ltc_public_client.send_bulk(
        TEST_LTC_WALLET_PRIVATE_KEY,
        {
            "mq2PZs9p5ZNLbu23KLKb1tdQt1mrBJM7CX": amount,
            "tltc1qshy0jeejm4pw3ep4cedc5vlmxyz348epnk7etf": amount,
        },
        deduct_fee=True,
    )

    utxo_list = await ltc_public_client.monitor._get_utxo_data(TEST_LTC_ADDRESS)
    assert len(utxo_list) == 1
    assert (
        utxo_list[0].tx_id
        == "e328d42e61f6b022c1534cd2e7e184180574172c988bea359f0b8e8734f178c6"
    )
    assert utxo_list[0].amount_satoshi == 42397453
    assert tx_id == "e328d42e61f6b022c1534cd2e7e184180574172c988bea359f0b8e8734f178c6"


@vcr_c.use_cassette("ltc/test_zero_balance_error.yaml")
async def test_zero_balance_error(ltc_public_client: AioTxLTCClient):
    await ltc_public_client.monitor._add_new_address(TEST_LTC_ADDRESS)
    amount = ltc_public_client.to_satoshi(0.005)
    with pytest.raises(InsufficientFunds) as excinfo:
        await ltc_public_client.send(
            TEST_LTC_WALLET_PRIVATE_KEY, "mq2PZs9p5ZNLbu23KLKb1tdQt1mrBJM7CX", amount
        )
    assert (
        str(excinfo.value)
        == "We have only 0 satoshi and it's 500000 at least needed to cover that transaction!"
    )


@vcr_c.use_cassette("ltc/test_not_enough_balance_error.yaml")
async def test_not_enough_balance_error(ltc_public_client: AioTxLTCClient):
    await ltc_public_client.monitor._add_new_address(TEST_LTC_ADDRESS)
    utxo_amount = ltc_public_client.to_satoshi(0.005)
    await ltc_public_client.monitor._add_new_utxo(
        TEST_LTC_ADDRESS,
        "3f7e5e1a897b6698d551f2b576d15eda85bf1c0d2706f7cb8c4b17a75632d1d2",
        utxo_amount,
        0,
    )
    amount = ltc_public_client.to_satoshi(0.01)
    with pytest.raises(InsufficientFunds) as excinfo:
        await ltc_public_client.send(
            TEST_LTC_WALLET_PRIVATE_KEY, "mq2PZs9p5ZNLbu23KLKb1tdQt1mrBJM7CX", amount
        )
    assert (
        str(excinfo.value)
        == "We have only 500000 satoshi and it's 1000000 at least needed to cover that transaction!"
    )


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Skipping transaction signing tests on Windows because we are not using RFC6979 from fastecdsa by default",
)
@vcr_c.use_cassette("ltc/send_few_single_transactions.yaml")
async def test_send_few_single_transactions(ltc_public_client: AioTxLTCClient):
    await ltc_public_client.monitor._add_new_address(TEST_LTC_ADDRESS)
    utxo_amount = ltc_public_client.to_satoshi(0.005)
    await ltc_public_client.monitor._add_new_utxo(
        TEST_LTC_ADDRESS,
        "89596bf8624118c6c3cd8cc2ebb6a2e19bc1c97abf994de9f23b8a2aef6765c1",
        utxo_amount,
        2,
    )
    amount = ltc_public_client.to_satoshi(0.01)
    with pytest.raises(InsufficientFunds) as excinfo:
        await ltc_public_client.send(
            TEST_LTC_WALLET_PRIVATE_KEY, TEST_LTC_ADDRESS, amount
        )
    assert (
        str(excinfo.value)
        == "We have only 500000 satoshi and it's 1000000 at least needed to cover that transaction!"
    )

    await ltc_public_client.monitor._add_new_utxo(
        TEST_LTC_ADDRESS,
        "c2f8e76c9537e5defa921b31edeb269603b8adec025c04d8e8b0e5764b80b861",
        utxo_amount,
        2,
    )

    tx_id = await ltc_public_client.send(
        TEST_LTC_WALLET_PRIVATE_KEY, TEST_LTC_ADDRESS, amount, deduct_fee=True
    )
    utxo_list = await ltc_public_client.monitor._get_utxo_data(TEST_LTC_ADDRESS)
    assert len(utxo_list) == 1
    assert (
        utxo_list[0].tx_id
        == "477ff66cdf3c97661c66d38a05cfae018d0358fec300a8b85bde65808e6cf8f9"
    )
    assert utxo_list[0].amount_satoshi == 997636
    assert tx_id == "477ff66cdf3c97661c66d38a05cfae018d0358fec300a8b85bde65808e6cf8f9"

    await ltc_public_client.monitor._mark_utxo_used(
        "477ff66cdf3c97661c66d38a05cfae018d0358fec300a8b85bde65808e6cf8f9", 0
    )

    with pytest.raises(InsufficientFunds) as excinfo:
        await ltc_public_client.send(
            TEST_LTC_WALLET_PRIVATE_KEY, TEST_LTC_ADDRESS, amount
        )
    assert (
        str(excinfo.value)
        == "We have only 0 satoshi and it's 1000000 at least needed to cover that transaction!"
    )

    await ltc_public_client.monitor._add_new_utxo(
        TEST_LTC_ADDRESS,
        "8117d7261873ab0bb49e195043d70693362cebe3275333678da5f738932bb3a7",
        utxo_amount,
        2,
    )

    await ltc_public_client.monitor._add_new_utxo(
        TEST_LTC_ADDRESS,
        "ad83a8dedeb35659cfc65053021125618ebdd0f60ee3b946fda5ea77df6a0047",
        utxo_amount,
        2,
    )

    await ltc_public_client.monitor._add_new_utxo(
        TEST_LTC_ADDRESS,
        "a51a47a487ab537dbf263d70a4ffd4535b57f479ba792c1549c4a4e9a44fcfb2",
        utxo_amount,
        2,
    )
    second_tx_amount = ltc_public_client.to_satoshi(0.012)
    tx_id = await ltc_public_client.send(
        TEST_LTC_WALLET_PRIVATE_KEY, TEST_LTC_ADDRESS, second_tx_amount
    )
    utxo_list = await ltc_public_client.monitor._get_utxo_data(TEST_LTC_ADDRESS)
    assert len(utxo_list) == 2
    balance = await ltc_public_client.get_balance(TEST_LTC_ADDRESS)
    assert balance == 296321 + 1200000
    assert tx_id == "09dac3c34ce8013a074890cdc34f90e264fda192b995350b7ad6d283f7d9276d"


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Skipping transaction signing tests on Windows because we are not using RFC6979 from fastecdsa by default",
)
@vcr_c.use_cassette("ltc/send_with_fee_per_byte.yaml")
async def test_send_with_fee_per_byte(ltc_public_client: AioTxLTCClient):
    await ltc_public_client.monitor._add_new_address(TEST_LTC_ADDRESS)
    await ltc_public_client.monitor._add_new_utxo(
        TEST_LTC_ADDRESS,
        "45d11c95718b39f52e11cddd69ce5be0585398afa299f0d7ab1e1ef7aa48ce5d",
        50000,
        1,
    )
    tx_id = await ltc_public_client.send(
        TEST_LTC_WALLET_PRIVATE_KEY,
        "mq2PZs9p5ZNLbu23KLKb1tdQt1mrBJM7CX",
        50000,
        deduct_fee=True,
        fee_per_byte=201,
    )
    utxo_list = await ltc_public_client.monitor._get_utxo_data(TEST_LTC_ADDRESS)
    assert len(utxo_list) == 0
    assert tx_id == "d2ed7d677005319439b4eb1a17cd66bd4cf32eea98d2b951352d627e4be9e340"


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Skipping transaction signing tests on Windows because we are not using RFC6979 from fastecdsa by default",
)
@vcr_c.use_cassette("ltc/send_with_fee_per_byte2.yaml")
async def test_send_with_fee_per_byte2(ltc_public_client: AioTxLTCClient):
    await ltc_public_client.monitor._add_new_address(TEST_LTC_ADDRESS)
    await ltc_public_client.monitor._add_new_utxo(
        TEST_LTC_ADDRESS,
        "477ff66cdf3c97661c66d38a05cfae018d0358fec300a8b85bde65808e6cf8f9",
        997636,
        0,
    )
    tx_id = await ltc_public_client.send(
        TEST_LTC_WALLET_PRIVATE_KEY,
        "mq2PZs9p5ZNLbu23KLKb1tdQt1mrBJM7CX",
        997636,
        deduct_fee=True,
        fee_per_byte=505,
    )
    utxo_list = await ltc_public_client.monitor._get_utxo_data(TEST_LTC_ADDRESS)
    assert len(utxo_list) == 0
    assert tx_id == "b9d298d1af00740332d663d2902d30453781447e13ef0cc6aa07d2922df12f61"


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Skipping transaction signing tests on Windows because we are not using RFC6979 from fastecdsa by default",
)
@pytest.mark.mysql
@vcr_c.use_cassette("ltc/monitoring_balance_send_mark_as_used.yaml")
async def test_monitoring_balance_send_mark_as_used(ltc_client_mysql: AioTxLTCClient):
    """
    Mega test :D It's for getting UTXO from monitoring (how it will be done by user)
    Checking balance, getting and checking UTXO list and sending transaction, checking what UTXO's was flagged
    as used
    """

    blocks = []
    transactions = []

    @ltc_client_mysql.monitor.on_block
    async def handle_block(block):
        blocks.append(block)

    @ltc_client_mysql.monitor.on_transaction
    async def handle_transaction(transaction):
        transactions.append(transaction)

    await ltc_client_mysql.import_address(TEST_LTC_ADDRESS, 3262692)
    asyncio.create_task(ltc_client_mysql.start_monitoring())

    try:
        await asyncio.sleep(2)
    except KeyboardInterrupt:
        ltc_client_mysql.stop_monitoring()

    assert len(blocks) > 0
    assert len(transactions) > 0
    assert 3262692 in blocks

    assert "a51a47a487ab537dbf263d70a4ffd4535b57f479ba792c1549c4a4e9a44fcfb2" in [
        tx["txid"] for tx in transactions
    ]

    # Removing some transaction from block 3262692 because we know they was used, but not monitoring in that test case
    await ltc_client_mysql.monitor._mark_utxo_used(
        "8117d7261873ab0bb49e195043d70693362cebe3275333678da5f738932bb3a7", 2
    )
    await ltc_client_mysql.monitor._mark_utxo_used(
        "89596bf8624118c6c3cd8cc2ebb6a2e19bc1c97abf994de9f23b8a2aef6765c1", 2
    )
    await ltc_client_mysql.monitor._mark_utxo_used(
        "a51a47a487ab537dbf263d70a4ffd4535b57f479ba792c1549c4a4e9a44fcfb2", 2
    )
    await ltc_client_mysql.monitor._mark_utxo_used(
        "ad83a8dedeb35659cfc65053021125618ebdd0f60ee3b946fda5ea77df6a0047", 2
    )
    await ltc_client_mysql.monitor._mark_utxo_used(
        "c2f8e76c9537e5defa921b31edeb269603b8adec025c04d8e8b0e5764b80b861", 2
    )

    tx_id = await ltc_client_mysql.send(
        TEST_LTC_WALLET_PRIVATE_KEY,
        "mq2PZs9p5ZNLbu23KLKb1tdQt1mrBJM7CX",
        10000,
        deduct_fee=True,
    )
    assert tx_id == "e9830d6d57c3a77a8d64c0df1a44eccdb0eeed6ef8fda66fb82d113c45dff6a1"


@pytest.mark.mysql
@vcr_c.use_cassette("ltc/big_integer_field_for_satoshi_check.yaml")
async def test_big_integer_field_for_satoshi_check(ltc_client_mysql: AioTxLTCClient):
    await ltc_client_mysql.import_address(TEST_LTC_ADDRESS, 3262692)
    utxo_value_balance = 317013443500
    await ltc_client_mysql.monitor._add_new_utxo(
        TEST_LTC_ADDRESS,
        "55863cc61de0c6c1c87282d3d6fb03650c0fc90ed3282191c618069cbde1d525",
        utxo_value_balance,
        0,
    )
    balance = await ltc_client_mysql.get_balance(TEST_LTC_ADDRESS)
    assert balance == utxo_value_balance


@pytest.mark.parametrize(
    "tx_id, expected_exception, expected_fee",
    [
        (
            "9ae506a01d89213bb84c91f5fd4365f7bc62b70bb61f30ec1d877bbf84600c30",
            NotImplementedError,
            0,
        ),
        ("c966837e3a29863341e3e85702152f479e97cd80e63684ddb2061c7c5cf92851", None, 534),
        (
            "3fcd11698664ffea5fe00adef6bd2c1c35de66c3fafb50f9076c74ff13fea139",
            None,
            500000,
        ),
        ("503112c3b7958161a45ceaf9d6ba5208d90849c641d2fad36f1c254ae11988b3", None, 534),
        ("c3623c6865885879bd4f908b9a97a77cbaf20a738675571a5af8bfd277c56a24", None, 0),
        (
            "55863cc61de0c6c1c87282d3d6fb03650c0fc90ed3282191c618069cbde1d525",
            None,
            500000,
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
@vcr_c.use_cassette("ltc/get_tx_fee.yaml")
async def test_get_tx_fee(
    ltc_public_client: AioTxLTCClient, tx_id, expected_exception, expected_fee
):
    if expected_exception:
        with pytest.raises(expected_exception):
            await ltc_public_client.get_tx_fee(tx_id)
    else:
        fee = await ltc_public_client.get_tx_fee(tx_id)
        assert isinstance(fee, int)
        assert fee == expected_fee


@pytest.mark.parametrize(
    "tx_id, expected_exception",
    [
        (
            "9ae506a01d89213bb84c91f5fd4365f7bc62b70bb61f30ec1d877bbf84600c30",
            None,
        ),
        (
            "c966837e3a29863341e3e85702152f479e97cd80e63684ddb2061c7c5cf92851",
            None,
        ),
        (
            "503112c3b7958161a45ceaf9d6ba5208d90849c641d2fad36f1c254ae11988b3",
            None,
        ),
        (
            "863cc61de0c6c1c87282d3d6fb03650c0fc90ed3282191c618069cbde1d525",
            RpcConnectionError,
        ),
        (
            "55863cc61de0c6c1c87282d3d6fb03650c0fc90ed3282191c618069cbde1d5",
            RpcConnectionError,
        ),
    ],
)
@vcr_c.use_cassette("ltc/get_raw_transaction.yaml")
async def test_get_raw_transaction(
    ltc_public_client: AioTxLTCClient, tx_id, expected_exception
):
    if expected_exception:
        with pytest.raises(expected_exception):
            await ltc_public_client.get_raw_transaction(tx_id)
    else:
        tx_data = await ltc_public_client.get_raw_transaction(tx_id)
        assert isinstance(tx_data, dict)
        assert "txid" in tx_data.keys()
