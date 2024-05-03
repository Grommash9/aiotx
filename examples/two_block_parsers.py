from aiotx.clients import AioTxBSCClient
import asyncio

client = AioTxBSCClient("NODE_URL", 97)
client2 = AioTxBSCClient("NODE_URL", 97)

@client.monitor.on_block
def handle_block(block):
    print("block", block)

@client.monitor.on_transaction
def handle_transaction(transaction):
    print("transaction", transaction)

@client2.monitor.on_block
def handle_block(block):
    print("client2: block", block)

@client2.monitor.on_transaction
def handle_transaction(transaction):
    print("client2: transaction", transaction)

async def main():
    monitoring_task1 = asyncio.create_task(client.start_monitoring(584))
    monitoring_task2 = asyncio.create_task(client2.start_monitoring(900))
    await asyncio.gather(monitoring_task1, monitoring_task2)

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        client.stop_monitoring()
        client2.stop_monitoring()


if __name__ == "__main__":
    asyncio.run(main())