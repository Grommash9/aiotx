import asyncio
import time
from confest import vcr_c, bsc_client
from aiotx.clients import AioTxBSCClient

@vcr_c.use_cassette("tests/fixtures/cassettes/bsc/test_monitoring.yaml")
def test_monitoring(bsc_client: AioTxBSCClient):
    blocks = []
    transactions = []

    @bsc_client.monitor.on_block
    def handle_block(block):
        blocks.append(block)

    @bsc_client.monitor.on_transaction
    def handle_transaction(transaction):
        transactions.append(transaction)

    bsc_client.start_monitoring(584)

    time.sleep(3)

    bsc_client.stop_monitoring()

    # Check the received blocks and transactions
    assert len(blocks) > 0
    assert len(transactions) > 0

    # Additional assertions based on your expectations
    # For example, you can check specific block numbers or transaction hashes
    assert 584 in blocks
    assert 585 in blocks
    assert "0x2a9d5aea2c8e4759e4e664f48e0dac79e76cb024e670251ddb2788144cee6f43" in [tx["hash"] for tx in transactions]
    assert "0xa45ccbf3c820f7bec2809461a8b7f1856246ed3b650ec2840bfbc303f118b76c" in [tx["hash"] for tx in transactions]


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

    bsc_client.start_monitoring(584)

    await asyncio.sleep(3)

    bsc_client.stop_monitoring()

    assert len(blocks) > 0
    assert len(transactions) > 0

    assert 584 in blocks
    assert 585 in blocks
    assert "0x2a9d5aea2c8e4759e4e664f48e0dac79e76cb024e670251ddb2788144cee6f43" in [tx["hash"] for tx in transactions]
    assert "0xa45ccbf3c820f7bec2809461a8b7f1856246ed3b650ec2840bfbc303f118b76c" in [tx["hash"] for tx in transactions]