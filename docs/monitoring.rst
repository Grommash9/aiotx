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

To start monitoring, you can use the `start_monitoring` method of the AioTxBSCClient instance. 

You can optionally specify the starting block number from which to begin monitoring. 

If no starting block is provided, monitoring will start from the latest block.

You can also use the `timeout_between_blocks` param for choose how much time monitoring should wait to try get new block.
In BTC for example we can wait 5-10 seconds and it's fine, but for TON we should wait <1 second

`timeout_between_blocks` is optional and set to 1 second by default

    - **monitoring_start_block** (int, optional): Block number from which to begin monitoring.
    - **timeout_between_blocks** (int, optional): How much seconds monitoring should wait to try get new block

.. code-block:: python

    await bsc_client.start_monitoring(
        monitoring_start_block=584, 
        timeout_between_blocks=2)

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

Here's the documentation for the `TonMonitor` class and the associated blockchain monitoring functionality:

Monitoring TON Blockchain
^^^^^^^^^^^^^^^^^^^^^^^^^

To monitor the TON blockchain, you need to create an instance of `AioTxTONClient` and use the `TonMonitor` class to start monitoring.

.. code-block:: python

    from aiotx.clients import AioTxTONClient
    import asyncio

    ton_client = AioTxTONClient("https://go.getblock.io/<token>")

    @ton_client.monitor.on_block
    async def handle_block(block):
        # Process the master block
        print("ton_client: block", block)

    @ton_client.monitor.on_transaction
    async def handle_transaction(transaction):
        # Process the transaction
        print("ton_client: transaction", transaction)

    async def main():
        await ton_client.start_monitoring()
        while True:
            await asyncio.sleep(1)

    if __name__ == "__main__":
        asyncio.run(main())

Output:

.. code-block:: text

    ton_client: transaction {'@type': 'blocks.shortTxId', 'mode': 135, 'account': '0:ffbd85ffba92089f5263a510ae89b7a8b0bc8bbea7c76102fb7154a4e84de04b', 'lt': '46762307000001', 'hash': 'uXqQz3LEJjor09cIcZ4IoRQX+IGuVnjBR1zQzut1tKY='}
    ton_client: block 38104588ton_client: block 38104588

In this example, we create an instance of `AioTxTONClient` with the appropriate API endpoint. We then register handlers for blocks and transactions using the `on_block` and `on_transaction` decorators, respectively.

Inside the `handle_block` handler, you can process the master block as needed. The `block` parameter contains the block data.

Inside the `handle_transaction` handler, you can process each transaction encountered. The `transaction` parameter contains basic transaction information such as the account address, logical time, and transaction hash.

By default, the transaction details are not fetched for every transaction to avoid consuming a large number of API calls. If you want to retrieve more details about a specific transaction, you can use the `get_transactions` method of `AioTxTONClient`, as shown in the example:

.. code-block:: python

    tx_details = await ton_client.get_transactions(
        "0:ffbd85ffba92089f5263a510ae89b7a8b0bc8bbea7c76102fb7154a4e84de04b",
        1, 46762307000001, "uXqQz3LEJjor09cIcZ4IoRQX+IGuVnjBR1zQzut1tKY=")

This allows you to selectively fetch transaction details for the transactions you are interested in.

Finally, the `main` function starts the monitoring process by calling `start_monitoring` on the `ton_client` instance. It then enters a loop to keep the script running and allow the monitoring to continue.

Note: Make sure to replace `<token>` in the API endpoint with your actual API token.

With this setup, you can monitor the TON blockchain, handle blocks and transactions, and selectively fetch transaction details as needed.