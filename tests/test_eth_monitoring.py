import asyncio

from conftest import vcr_c

from aiotx.clients import AioTxBSCClient


@vcr_c.use_cassette("tests/fixtures/cassettes/eth/test_async_monitoring.yaml")
async def test_async_monitoring(eth_client: AioTxBSCClient):
    blocks = []
    transactions = []

    @eth_client.monitor.on_block
    async def handle_block(block):
        blocks.append(block)

    @eth_client.monitor.on_transaction
    async def handle_transaction(transaction):
        transactions.append(transaction)

    await eth_client.start_monitoring(2834064)
    try:
        await asyncio.sleep(3)
    except KeyboardInterrupt:
        eth_client.stop_monitoring()

    assert len(blocks) > 0
    assert len(transactions) > 0

    assert 2834064 in blocks
    assert 2834065 in blocks
    assert "0x5b6fd8fda590e887531df12dec5faf2ce8c94a3eeb56bcc1fde760fabd64e56e" in [tx["hash"] for tx in transactions]
    assert "0x10f4376f7efe2637be4d012eebad143dce58626146befa48204f1275476064d6" in [tx["hash"] for tx in transactions]

    for tx in transactions:
        assert "aiotx_decoded_input" in tx.keys()
