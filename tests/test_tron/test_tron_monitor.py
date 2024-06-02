import asyncio

from conftest import vcr_c

from aiotx.clients import AioTxBSCClient


@vcr_c.use_cassette("tests/fixtures/cassettes/tron/test_async_monitoring.yaml")
async def test_async_monitoring(tron_client: AioTxBSCClient):
    blocks = []
    transactions = []

    @tron_client.monitor.on_block
    async def handle_block(block):
        blocks.append(block)

    @tron_client.monitor.on_transaction
    async def handle_transaction(transaction):
        transactions.append(transaction)

    await tron_client.start_monitoring(47338868)
    try:
        await asyncio.sleep(3)
    except KeyboardInterrupt:
        tron_client.stop_monitoring()

    assert len(blocks) > 0
    assert len(transactions) > 0

    assert 47338868 in blocks
    assert 47338869 in blocks
    assert 47338870 in blocks

    # TRX transfer from block 47338868
    assert "0x72ce7a6a1bfdaca67431e96857cb17dc1c86bbe36cfefb4bab7ed72f7e72122c" in [tx["hash"] for tx in transactions]

    #TRC20 transaction from block 47338870
    assert "0x2ee04f0cc089e1f1d2499c1f7ee3114a69a61dda478c39ea2d1becdd97d387fa" in [tx["hash"] for tx in transactions]
    assert "0xc00858d686c1433369815ba366610b84064cbc4a684284887ccbf2091ed80558" in [tx["hash"] for tx in transactions]
    
    for tx in transactions:
        assert "aiotx_decoded_input" in tx.keys()
