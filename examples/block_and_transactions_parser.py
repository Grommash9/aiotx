from aiotx.clients import AioTxBSCClient
import asyncio

client = AioTxBSCClient("NODE_URL", 97)

@client.monitor.on_block
def handle_block(block):
    print("block", block)

@client.monitor.on_transaction
def handle_transaction(transaction):
    print("transaction", transaction)


async def main():
    await client.start_monitoring(584)

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        client.stop_monitoring()


if __name__ == "__main__":
    asyncio.run(main())