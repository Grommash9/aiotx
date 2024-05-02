from aiogram import Bot, Dispatcher
from aiotx.clients import AioTxBSCClient
import asyncio

# Create an instance of the aiogram bot
bot = Bot(token="7109548724:AAFBU_TLOywlm2GuC0gV2rYSiYe09HjP84E")
dispatcher = Dispatcher()

# Create an instance of the AioTxBSCClient
client = AioTxBSCClient("https://nameless-flashy-snow.bsc-testnet.quiknode.pro/c54e248a38fb9b7a8b31d84d57c1e41b203ed019/", 97)

# Define the block handler
@client.monitor.on_block
async def handle_block(block):
    block_number = block
    chat_id = "5454053704"  # Replace with the actual chat ID
    message = f"New block: {block_number}"
    await bot.send_message(chat_id=chat_id, text=message)

# Define the transaction handler (optional)
@client.monitor.on_transaction
async def handle_transaction(transaction):
    transaction_hash = transaction["hash"]
    chat_id = "5454053704"  # Replace with the actual chat ID
    message = f"New transaction: {transaction_hash}"
    await bot.send_message(chat_id=chat_id, text=message)

# Start the monitoring process
client.start_monitoring(584)

# Start the aiogram bot
asyncio.run(dispatcher.start_polling(bot))