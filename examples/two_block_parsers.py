import asyncio

from aiotx.clients import AioTxBSCClient, AioTxETHClient

BSC_TEST_NODE_URL = "https://bsc-testnet-rpc.publicnode.com"
ETH_TEST_NODE_URL = "https://ethereum-sepolia-rpc.publicnode.com"

bsc_client = AioTxBSCClient(BSC_TEST_NODE_URL)
eth_client = AioTxETHClient(ETH_TEST_NODE_URL)


@bsc_client.monitor.on_block
async def handle_block(block, latest_block):
    print("bsc_client: block", block)


@bsc_client.monitor.on_transaction
async def handle_transaction(transaction):
    print("bsc_client: transaction", transaction)


@eth_client.monitor.on_block
async def handle_block(block, latest_block):
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
