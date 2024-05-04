import asyncio

from conftest import vcr_c

from aiotx.clients import AioTxBTCClient


@vcr_c.use_cassette("btc/test_async_monitoring.yaml")
async def test_async_monitoring(btc_client: AioTxBTCClient):
    blocks = []
    transactions = []

    @btc_client.monitor.on_block
    async def handle_block(block):
        blocks.append(block)

    @btc_client.monitor.on_transaction
    async def handle_transaction(transaction):
        transactions.append(transaction)

    await btc_client.start_monitoring(555)
    try:
        await asyncio.sleep(3)
    except KeyboardInterrupt:
        btc_client.stop_monitoring()

    assert len(blocks) > 0
    assert len(transactions) > 0

    assert 555 in blocks
    assert 556 in blocks
    assert "070a808197d97c8982587f75fef6d531282863a110ad5e8b42cdec8ddb6dc4e0" in [tx["txid"] for tx in transactions]
    assert "c852040a873a8f3c1ee69fda40dcf32a118978a923f62176272e840fc042de54" in [tx["txid"] for tx in transactions]


