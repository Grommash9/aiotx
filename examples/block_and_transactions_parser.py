from aiotx.clients import AioTxBSCClient

client = AioTxBSCClient("NODE_URL", 97)


@client.monitor.on_block
def handle_block(block):
    print("block", block)


@client.monitor.on_transaction
def handle_transaction(transaction):
    print("transaction", transaction)


client.start_monitoring()
