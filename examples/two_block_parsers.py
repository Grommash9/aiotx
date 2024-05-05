from aiotx.clients import AioTxBSCClient, AioTxETHClient
import asyncio

bsc_client = AioTxBSCClient("NODE_URL", 97)
eth_client = AioTxETHClient("NODE_URL", 1151511)

@bsc_client.monitor.on_block
async def handle_block(block):
    print("bsc_client: block", block)

@bsc_client.monitor.on_transaction
async def handle_transaction(transaction):
    print("bsc_client: transaction", transaction)

@eth_client.monitor.on_block
async def handle_block(block):
    print("eth_client: block", block)

@eth_client.monitor.on_transaction
async def handle_transaction(transaction):
    print("eth_client: transaction", transaction)

async def main():
    monitoring_task1 = asyncio.create_task(bsc_client.start_monitoring(584))
    monitoring_task2 = asyncio.create_task(eth_client.start_monitoring(900))
    await asyncio.gather(monitoring_task1, monitoring_task2)

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        bsc_client.stop_monitoring()
        eth_client.stop_monitoring()


if __name__ == "__main__":
    asyncio.run(main())