import asyncio

from aiotx.clients import AioTxETHClient

eth_client = AioTxETHClient(node_url="https://ethereum-sepolia-rpc.publicnode.com")


@eth_client.monitor.on_block
async def handle_block(block):
    print("eth_client: block", block)


@eth_client.monitor.on_transaction
async def handle_transaction(transaction):
    print("eth_client: transaction", transaction)


async def main():
    await eth_client.start_monitoring()
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
