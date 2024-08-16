import asyncio

from aiotx.clients import AioTxETHClient

eth_client = AioTxETHClient(node_url="https://ethereum-sepolia-rpc.publicnode.com")


@eth_client.monitor.on_block
async def handle_block(cur_block, latest_block):
    print("eth_client: block", cur_block, latest_block)


@eth_client.monitor.on_transaction
async def handle_transaction(transaction):
    print("eth_client: transaction", transaction)


# You can use handler for get all block transactions as well
@eth_client.monitor.on_block_transactions
async def handle_block_transactions(transactions):
    print("eth_client: block transactions list", transactions)


async def main():
    await eth_client.start_monitoring()


if __name__ == "__main__":
    asyncio.run(main())
