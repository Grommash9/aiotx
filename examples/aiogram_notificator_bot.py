import asyncio

from aiogram import Bot, Dispatcher

from aiotx.clients import AioTxBSCClient

# Create an instance of the aiogram bot
bot = Bot(token="BOT TOKEN")
dispatcher = Dispatcher()

# Create an instance of the AioTxBSCClient
client = AioTxBSCClient("NODE URL", 97)


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
client.start_monitoring()

# Start the aiogram bot
asyncio.run(dispatcher.start_polling(bot))
