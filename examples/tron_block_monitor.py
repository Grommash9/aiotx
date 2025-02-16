import asyncio

from aiotx.clients import AioTxTRONClient



tron_client = AioTxTRONClient(node_url="https://api.tatum.io/v3/blockchain/node/tron-mainnet/t-67582927d04074ce31f00511-79b14eb9451148ccbf00b7c3")


@tron_client.monitor.on_block
async def handle_block(block, last_block):
    print("tron_client: block", block, last_block)


@tron_client.monitor.on_transaction
async def handle_transaction(transaction):
    print("tron_client: transaction", transaction)


async def main():
    await tron_client.connect()
    block_data = await tron_client.start_monitoring()
    # print(block_data)

if __name__ == "__main__":
    asyncio.run(main())
