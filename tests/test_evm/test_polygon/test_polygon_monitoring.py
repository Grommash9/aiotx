import asyncio

from conftest import vcr_c

from aiotx.clients import AioTxPolygonClient


@vcr_c.use_cassette("tests/fixtures/cassettes/polygon/test_async_monitoring.yaml")
async def test_async_monitoring(polygon_client: AioTxPolygonClient):
    blocks = []
    transactions = []

    @polygon_client.monitor.on_block
    async def handle_block(block):
        blocks.append(block)

    @polygon_client.monitor.on_transaction
    async def handle_transaction(transaction):
        transactions.append(transaction)

    await polygon_client.start_monitoring(7385898)
    try:
        await asyncio.sleep(3)
    except KeyboardInterrupt:
        polygon_client.stop_monitoring()

    assert len(blocks) > 0
    assert len(transactions) > 0

    assert 7385898 in blocks
    assert 7385899 in blocks
    assert "0x568435d3c40e00160885d9030f231adfc230c91a5dab740515e89e30600a734c" in [
        tx["hash"] for tx in transactions
    ]
    assert "0x1913ae3314b38254c07538910ebdf2e3a3d6562b084769ef6614a0f0f4e01367" in [
        tx["hash"] for tx in transactions
    ]

    for tx in transactions:
        assert "aiotx_decoded_input" in tx.keys()
