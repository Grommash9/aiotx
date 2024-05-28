TON client
==========

Introduction
------------

The TON (The Open Network) Client is a powerful tool for interacting with the TON blockchain. It provides a seamless way to connect to the TON network, perform various operations, and monitor blockchain activities.

The TON Client supports the TON cryptocurrency and offers a range of functionalities, including wallet creation, balance retrieval, transaction history, and sending transactions.

QuickStart
----------

To get started with the TON Client, you need to create an instance of `AioTxTONClient` by providing the TON node URL. Here's an example:

.. code-block:: python

   from aiotx.clients import AioTxTONClient
   import asyncio

   async def main():
      ton_client = AioTxTONClient("https://ton.getblock.io/<token>/jsonRPC")

      # Create a new wallet
      memo, address, raw_address = await ton_client.generate_address()
      print("New wallet address:", address)

      # Get wallet balance
      balance = await ton_client.get_balance(address)
      print("Wallet balance:", ton_client.from_nano(balance, "ton"), "TON")

      # Get transaction history
      transactions = await ton_client.get_transactions(address, limit=10)
      print("Recent transactions:")
      for tx in transactions:
         print("  - Transaction ID:", tx["transaction_id"]["hash"])
         print("    Amount:", ton_client.from_nano(int(tx["in_msg"]["value"]), "ton"), "TON")

      # Send TON
      to_address = "EQDvRVnNMFgg8Wc4UZqVb8lnsTrPVwdX0-mYu_SdPzt0dIWX"
      amount = ton_client.to_nano(1.5)  # 1.5 TON
      tx_hash = await ton_client.send(mnemonic, to_address, amount)
      print("Transaction sent. Hash:", tx_hash)

   asyncio.run(main())

In this example, we create an instance of `AioTxTONClient` by providing the TON node URL. Make sure to replace `<token>` with your actual API token.

The code demonstrates the following operations:

1. Creating a new wallet by generating a mnemonic phrase and deriving the wallet address from it.
2. Retrieving the balance of the wallet using the `get_balance` method.
3. Fetching the recent transaction history of the wallet using the `get_transactions` method.
4. Sending TON to another address using the `send` method.

Blockchain Monitoring
---------------------

You can monitor the TON blockchain for new blocks and transactions in real-time. This feature is particularly useful for tracking specific addresses or detecting certain events.

For detailed information on how to set up and use blockchain monitoring with the TON Client, please refer to the :doc:`../../monitoring`.

Methods
-------

.. toctree::
   :maxdepth: 1

   generate_address
   get_balance
   get_transactions
   to_nano
   from_nano
   send
   