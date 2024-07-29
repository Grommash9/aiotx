import asyncio

from conftest import vcr_c

from aiotx.clients import AioTxLTCClient


@vcr_c.use_cassette("tests/fixtures/cassettes/ltc/test_async_monitoring.yaml")
async def test_async_monitoring(ltc_public_client: AioTxLTCClient):
    blocks = []
    transactions = []
    block_transactions_list = []

    @ltc_public_client.monitor.on_block
    async def handle_block(block):
        blocks.append(block)

    @ltc_public_client.monitor.on_transaction
    async def handle_transaction(transaction):
        transactions.append(transaction)

    @ltc_public_client.monitor.on_block_transactions
    async def handle_block_transactions(transactions):
        block_transactions_list.append(transactions)

    await ltc_public_client.import_address(
        "tltc1qsawz44ppfnxmnat7635f83exgf9mynrzs5tsgl", 3247853
    )
    asyncio.create_task(ltc_public_client.start_monitoring())

    try:
        await asyncio.sleep(3)
    except KeyboardInterrupt:
        ltc_public_client.stop_monitoring()

    assert len(blocks) > 0
    assert len(transactions) > 0

    assert 3247853 in blocks
    assert 3247854 in blocks
    assert "7604930759225ab74868969da6b19b399d8b189bd9506f39e15019f8e08a1d44" in [
        tx["txid"] for tx in transactions
    ]
    assert "992b887a10aa924430e905174535fd92733136b76d39e835c109e3ff2719bd69" in [
        tx["txid"] for tx in transactions
    ]
    assert "7604930759225ab74868969da6b19b399d8b189bd9506f39e15019f8e08a1d44" in [
        tx["txid"] for tx in block_transactions_list[0]
    ]

    assert "992b887a10aa924430e905174535fd92733136b76d39e835c109e3ff2719bd69" in [
        tx["txid"] for tx in block_transactions_list[1]
    ]
