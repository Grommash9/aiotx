import asyncio

from conftest import vcr_c

from aiotx.clients import AioTxTONClient


@vcr_c.use_cassette(
    "tests/fixtures/cassettes/ton/test_async_monitoring_with_shard_gaps_case.yaml"
)
async def test_shard_block_skipping_monitoring_case(ton_client: AioTxTONClient):
    blocks = []
    transactions = []

    await ton_client.connect()

    @ton_client.monitor.on_block
    async def handle_block(block):
        blocks.append(block)

    @ton_client.monitor.on_transaction
    async def handle_transaction(transaction):
        transactions.append(transaction)

    asyncio.create_task(
        ton_client.start_monitoring(27411721, timeout_between_blocks=0.1)
    )
    # master block 27411723 have shard with seqno 29177784
    # master block 27411724 have shard with seqno 29177786
    # In that tests we are looking for transactions in shard 29177785
    try:
        await asyncio.sleep(3)
    except KeyboardInterrupt:
        ton_client.stop_monitoring()

    assert len(blocks) > 0
    assert len(transactions) > 0

    assert 27411722 in blocks
    assert 27411723 in blocks
    assert 27411724 in blocks

    # Our transaction from shard 29177785 which was skipped between 27411723 and 27411724 master blocks
    assert "hssG0zMQPV4wFBiiuqUd5iJZIt/gWFzFD0us7GMK8eM=" in [
        tx["hash"] for tx in transactions
    ]


@vcr_c.use_cassette("tests/fixtures/cassettes/ton/test_async_monitoring_testnet.yaml")
async def test_async_monitoring_testnet(ton_client: AioTxTONClient):
    blocks = []
    transactions = []

    await ton_client.connect()

    @ton_client.monitor.on_block
    async def handle_block(block):
        blocks.append(block)

    @ton_client.monitor.on_transaction
    async def handle_transaction(transaction):
        transactions.append(transaction)

    asyncio.create_task(
        ton_client.start_monitoring(19627949, timeout_between_blocks=0.1)
    )
    try:
        await asyncio.sleep(3)
    except KeyboardInterrupt:
        ton_client.stop_monitoring()

    assert len(blocks) > 0
    assert len(transactions) > 0

    assert 19627950 in blocks
    assert 19627951 in blocks
    assert 19627952 in blocks

    # we are not able to see that in block explorer tonscan, but we can see that in ton centre
    assert "FT1lZcFBL2rR3KYtz6m9nWTegS76u4kudfr+4stIxoU=" in [
        tx["hash"] for tx in transactions
    ]
    assert "jxP0qffivNEbR1SVgG2jZ5ds+Hk/aUKW0rmY0/Jso9Q=" in [
        tx["hash"] for tx in transactions
    ]
