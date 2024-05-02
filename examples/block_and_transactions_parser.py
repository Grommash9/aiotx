from aiotx.clients import AioTxBSCClient

# Create an instance of the AioTxBSCClient
client = AioTxBSCClient("https://nameless-flashy-snow.bsc-testnet.quiknode.pro/c54e248a38fb9b7a8b31d84d57c1e41b203ed019/", 97)

# Define the block handler
@client.monitor.on_block
async def handle_block(block):
    print("block", block)

# Define the transaction handler (optional)
@client.monitor.on_transaction
async def handle_transaction(transaction):
    print("transaction", transaction)

# Start the monitoring process
client.start_monitoring(584)