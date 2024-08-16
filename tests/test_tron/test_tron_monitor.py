import asyncio

from conftest import vcr_c

from aiotx.clients import AioTxBSCClient


@vcr_c.use_cassette("tests/fixtures/cassettes/tron/test_async_monitoring.yaml")
async def test_async_monitoring(tron_client: AioTxBSCClient):
    blocks = []
    transactions = []
    block_transactions_list = []

    @tron_client.monitor.on_block
    async def handle_block(block, latest_block):
        blocks.append(block)

    @tron_client.monitor.on_transaction
    async def handle_transaction(transaction):
        transactions.append(transaction)

    @tron_client.monitor.on_block_transactions
    async def handle_block_transactions(transactions):
        block_transactions_list.append(transactions)

    asyncio.create_task(tron_client.start_monitoring(44739341))
    try:
        await asyncio.sleep(3)
    except KeyboardInterrupt:
        tron_client.stop_monitoring()

    assert len(blocks) > 0
    assert len(transactions) > 0

    assert 44739341 in blocks
    assert 44739342 in blocks
    assert 44739343 in blocks

    # TRX transfer from block 44739341
    assert "0xb05b7aea5a92a03482af7b764a3c75c0c54de169abdff79d9cb4c4b545fa97a1" in [
        tx["hash"] for tx in transactions
    ]

    # TRC20 transaction from block 44739342
    assert "0x18ea751dac569c9143d679cd8f4c53680c94e336a1b54008b940212a54fbc491" in [
        tx["hash"] for tx in transactions
    ]
    assert "0xec4841f9675a0785c52cb8d7d2c3ca0aeedd4df4590ef4a94b4ca21b48ef11ae" in [
        tx["hash"] for tx in transactions
    ]

    # TRC20 transaction from block 44739343
    assert "0x48a89e3e068379761fdf2d0e2088ffe880803ac8de9e70632fc620b1450045ca" in [
        tx["hash"] for tx in transactions
    ]

    for tx in transactions:
        assert "aiotx_decoded_input" in tx.keys()

    assert "0xb05b7aea5a92a03482af7b764a3c75c0c54de169abdff79d9cb4c4b545fa97a1" in [
        tx["hash"] for tx in block_transactions_list[0]
    ]
    assert "0x18ea751dac569c9143d679cd8f4c53680c94e336a1b54008b940212a54fbc491" in [
        tx["hash"] for tx in block_transactions_list[1]
    ]
    assert "0xec4841f9675a0785c52cb8d7d2c3ca0aeedd4df4590ef4a94b4ca21b48ef11ae" in [
        tx["hash"] for tx in block_transactions_list[1]
    ]
    assert "0x48a89e3e068379761fdf2d0e2088ffe880803ac8de9e70632fc620b1450045ca" in [
        tx["hash"] for tx in block_transactions_list[2]
    ]

    for tx in block_transactions_list[0]:
        assert "aiotx_decoded_input" in tx.keys()
