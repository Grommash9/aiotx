import asyncio

from aiogram import Bot, Dispatcher

from aiotx.clients import AioTxBSCClient

# Create an instance of the aiogram bot
bot = Bot(token="BOT TOKEN")
dispatcher = Dispatcher()

# Create an instance of the AioTxBSCClient
bsc_client = AioTxBSCClient("https://bsc-testnet-rpc.publicnode.com")


# Define the block handler
@bsc_client.monitor.on_block
async def handle_block(block, latest_block):
    block_number = block
    chat_id = "5454053704"  # Replace with the actual chat ID
    message = f"New block: {block_number}"
    await bot.send_message(chat_id=chat_id, text=message)


# Define the transaction handler (optional)
@bsc_client.monitor.on_transaction
async def handle_transaction(transaction):
    transaction_hash = transaction["hash"]
    chat_id = "5454053704"  # Replace with the actual chat ID
    message = f"New transaction: {transaction_hash}"
    await bot.send_message(chat_id=chat_id, text=message)


async def main():
    monitoring_task = asyncio.create_task(bsc_client.start_monitoring(584))
    await asyncio.gather(monitoring_task, dispatcher.start_polling(bot))


if __name__ == "__main__":
    asyncio.run(main())
