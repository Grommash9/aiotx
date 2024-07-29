import asyncio

from aiotx.clients import AioTxLTCClient

ltc_client = AioTxLTCClient(
    node_url="https://api.tatum.io/v3/blockchain/node/litecoin-core-testnet",
    testnet=True,
)


@ltc_client.monitor.on_block
async def handle_block(block):
    print("ltc_client: block", block)


@ltc_client.monitor.on_transaction
async def handle_transaction(transaction):
    print("ltc_client: transaction", transaction)


async def main():
    await ltc_client.start_monitoring()


if __name__ == "__main__":
    asyncio.run(main())
