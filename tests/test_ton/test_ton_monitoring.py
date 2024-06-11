import asyncio

from conftest import vcr_c

from aiotx.clients import AioTxTONClient


@vcr_c.use_cassette("tests/fixtures/cassettes/ton/test_async_monitoring.yaml")
async def test_async_monitoring(ton_mainnet_client: AioTxTONClient):
    blocks = []
    transactions = []

    @ton_mainnet_client.monitor.on_block
    async def handle_block(block):
        blocks.append(block)

    @ton_mainnet_client.monitor.on_transaction
    async def handle_transaction(transaction):
        transactions.append(transaction)

    await ton_mainnet_client.start_monitoring(38093046, timeout_between_blocks=0.1)
    try:
        await asyncio.sleep(3)
    except KeyboardInterrupt:
        ton_mainnet_client.stop_monitoring()

    assert len(blocks) > 0
    assert len(transactions) > 0

    assert 38093046 in blocks
    assert 38093047 in blocks
    assert 38093048 in blocks

    # transactions from shard 43736268 of master block 38093046
    # https://tonscan.org/block/0:6000000000000000:43736268
    assert "r4r7FlGRAflxcnfEeDwVy1uqhEh/ajyZsUCgrwbATTY=" in [
        tx["hash"] for tx in transactions
    ]
    # transactions from shard 43736268 of master block 38093046
    assert "NZEK2M1V3VqEdhuEmj5qayWh2e0Sc/lEcOYGMpUDe0o=" in [
        tx["hash"] for tx in transactions
    ]

    # transactions from shard 43735772 of master block 38093046
    assert "ayDy6PrzGMCR4rMMD3FEThLEgjMB8heqmcUdJC3CI/A=" in [
        tx["hash"] for tx in transactions
    ]
    # transactions from shard 43735772 of master block 38093046
    assert "EPfqGpYOWZg1LpGQ06HfxFhxwwWNZKeQQtIAJ4U60Eg=" in [
        tx["hash"] for tx in transactions
    ]

    # transactions from shard 43736270 of master block 38093047
    assert "xcPkFFntBatwm/mC06Enl3tYZmCQhnfcQncZ0InbA3o=" in [
        tx["hash"] for tx in transactions
    ]

    # transactions from shard 43736027 of master block 38093047
    assert "WoQxVXUxtxC8nPdkvPdj0/wVTb6JkntyXg1fXxmdXQQ=" in [
        tx["hash"] for tx in transactions
    ]
    assert "/NiBkmuPCaFdu4pv+Y1oxdJ0dlOWkEgCFPf+Mg/S6LU=" in [
        tx["hash"] for tx in transactions
    ]
    assert "GKZ+EwkxxAONtWntnUTD/ISg2aZ2iy16XkVS/wiS3Lw=" in [
        tx["hash"] for tx in transactions
    ]


@vcr_c.use_cassette("tests/fixtures/cassettes/ton/test_async_monitoring_testnet.yaml")
async def test_async_monitoring_testnet(ton_client: AioTxTONClient):
    blocks = []
    transactions = []

    @ton_client.monitor.on_block
    async def handle_block(block):
        blocks.append(block)

    @ton_client.monitor.on_transaction
    async def handle_transaction(transaction):
        transactions.append(transaction)

    await ton_client.start_monitoring(19627950, timeout_between_blocks=0.1)
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
