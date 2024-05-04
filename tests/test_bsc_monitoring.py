import asyncio

from conftest import vcr_c

from aiotx.clients import AioTxBSCClient


@vcr_c.use_cassette("tests/fixtures/cassettes/bsc/test_async_monitoring.yaml")
async def test_async_monitoring(bsc_client: AioTxBSCClient):
    blocks = []
    transactions = []

    @bsc_client.monitor.on_block
    async def handle_block(block):
        blocks.append(block)

    @bsc_client.monitor.on_transaction
    async def handle_transaction(transaction):
        transactions.append(transaction)

    await bsc_client.start_monitoring(584)
    try:
        await asyncio.sleep(3)
    except KeyboardInterrupt:
        bsc_client.stop_monitoring()

    assert len(blocks) > 0
    assert len(transactions) > 0

    assert 584 in blocks
    assert 585 in blocks
    assert "0x2a9d5aea2c8e4759e4e664f48e0dac79e76cb024e670251ddb2788144cee6f43" in [tx["hash"] for tx in transactions]
    assert "0xa45ccbf3c820f7bec2809461a8b7f1856246ed3b650ec2840bfbc303f118b76c" in [tx["hash"] for tx in transactions]

    for tx in transactions:
        assert "aiotx_decoded_input" in tx.keys()
