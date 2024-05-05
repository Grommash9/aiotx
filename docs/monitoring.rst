Blockchain monitoring
============================

AioTx provides functionality to monitor new blocks and transactions on the blockchain. It allows you to register handlers that will be called when new blocks or transactions are detected.

Now it's working and checked for ETH, BSC, BTC and LTC

Registering Handlers
^^^^^^^^^^^^^^^^^^^^

You can register handlers for blocks and transactions using the `on_block` and `on_transaction` decorators provided by the `monitor` attribute of the AioTxBSCClient instance.

Block Handler
"""""""""""""

To register a block handler, use the `@client.monitor.on_block` decorator. The decorated function should accept a single parameter representing the block number. Here's an example:

.. code-block:: python

    @bsc_client.monitor.on_block
    async def handle_block(block):
        print("Block:", block)

Transaction Handler
"""""""""""""""""""

To register a transaction handler, use the `@client.monitor.on_transaction` decorator. The decorated function should accept a single parameter representing the transaction details. Here's an example:

.. code-block:: python

    @bsc_client.monitor.on_transaction
    async def handle_transaction(transaction):
        print("Transaction:", transaction)

Starting and Stopping Monitoring
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To start monitoring, you can use the `start_monitoring` method of the AioTxBSCClient instance. You can optionally specify the starting block number from which to begin monitoring. If no starting block is provided, monitoring will start from the latest block.

.. code-block:: python

    await bsc_client.start_monitoring(584)

To stop monitoring, you can use the `stop_monitoring` method.

.. code-block:: python

    bsc_client.stop_monitoring()

Monitoring Multiple Clients
^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can monitor multiple instances simultaneously by creating separate instances and registering handlers for each one. Here's an example:

.. code-block:: python

    from aiotx.clients import AioTxBSCClient, AioTxETHClient
    import asyncio

    bsc_client = AioTxBSCClient("NODE_URL", 97)
    eth_client = AioTxETHClient("NODE_URL", 1151511)

    @bsc_client.monitor.on_block
    async def handle_block(block):
        print("bsc_client: block", block)

    @bsc_client.monitor.on_transaction
    async def handle_transaction(transaction):
        print("bsc_client: transaction", transaction)

    @eth_client.monitor.on_block
    async def handle_block(block):
        print("eth_client: block", block)

    @eth_client.monitor.on_transaction
    async def handle_transaction(transaction):
        print("eth_client: transaction", transaction)

    async def main():
        bsc_task = asyncio.create_task(bsc_client.start_monitoring())
        eth_task = asyncio.create_task(eth_client.start_monitoring())
        await asyncio.gather(bsc_task, eth_task)

        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            bsc_client.stop_monitoring()
            eth_client.stop_monitoring()


    if __name__ == "__main__":
        asyncio.run(main())

Integration with Aiogram
^^^^^^^^^^^^^^^^^^^^^^^^

You can integrate the monitoring functionality with the Aiogram library to send notifications or perform actions based on the received blocks and transactions. Here's an example:

.. code-block:: python

    from aiogram import Bot, Dispatcher
    from aiotx.clients import AioTxBSCClient

    bot = Bot(token="BOT_TOKEN")
    dispatcher = Dispatcher()
    bsc_client = AioTxBSCClient("NODE_URL", 97)

    @bsc_client.monitor.on_block
    async def handle_block(block):
        block_number = block
        chat_id = "CHAT_ID"
        message = f"New block: {block_number}"
        await bot.send_message(chat_id=chat_id, text=message)

    async def main():
        monitoring_task = asyncio.create_task(bsc_client.start_monitoring())
        await asyncio.gather(monitoring_task, dispatcher.start_polling(bot))

    asyncio.run(main())

In this example, the `handle_block` function is called whenever a new block is received. It sends a message to the specified chat ID using the Aiogram bot.

These examples demonstrate different ways to utilize the monitoring functionality provided by AioTxBSCClient. You can customize the handlers and integrate monitoring into your application based on your specific requirements.