import asyncio

from conftest import vcr_c

from aiotx.clients import AioTxLTCClient


@vcr_c.use_cassette("tests/fixtures/cassettes/ltc/test_async_monitoring.yaml")
async def test_async_monitoring(ltc_public_client: AioTxLTCClient):
    blocks = []
    transactions = []

    @ltc_public_client.monitor.on_block
    async def handle_block(block):
        blocks.append(block)

    @ltc_public_client.monitor.on_transaction
    async def handle_transaction(transaction):
        transactions.append(transaction)

    await ltc_public_client.start_monitoring(3247853)
    try:
        await asyncio.sleep(3)
    except KeyboardInterrupt:
        ltc_public_client.stop_monitoring()

    assert len(blocks) > 0
    assert len(transactions) > 0

    assert 3247853 in blocks
    assert 3247854 in blocks
    assert 3247855 in blocks
    assert "7604930759225ab74868969da6b19b399d8b189bd9506f39e15019f8e08a1d44" in [tx["txid"] for tx in transactions]
    assert "cc2f6dcf37ee8cf019145c2a3eaabf70f14a42dd9aa5f31ed1baa549716fe7b9" in [tx["txid"] for tx in transactions]


