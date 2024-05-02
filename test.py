from aiotx.clients import AioTxBSCClient
import time

client = AioTxBSCClient("https://nameless-flashy-snow.bsc-testnet.quiknode.pro/c54e248a38fb9b7a8b31d84d57c1e41b203ed019/", 97, 584)


@client.monitor.on_block
def handle_block(block):
    print(f"New block: {block}")

@client.monitor.on_transaction
def handle_transaction(transaction):
    print(f"New transaction: {transaction}")


client.start_monitoring()

while True:
    print("working!!!!!")
    time.sleep(0.1)

client.stop_monitoring()