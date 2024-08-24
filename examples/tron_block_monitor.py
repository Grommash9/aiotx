import asyncio

from aiotx.clients import AioTxTRONClient

tron_client = AioTxTRONClient(node_url="https://api.shasta.trongrid.io")


@tron_client.monitor.on_block
async def handle_block(block, last_block):
    print("tron_client: block", block, last_block)


@tron_client.monitor.on_transaction
async def handle_transaction(transaction):
    print("tron_client: transaction", transaction)


async def main():
    await tron_client.start_monitoring(5)


if __name__ == "__main__":
    asyncio.run(main())
