.. AioTx documentation master file, created by
   sphinx-quickstart on Fri May 3 16:38:46 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to AioTx's documentation!
==================================

AioTx is a comprehensive Python package designed to simplify and streamline your cryptocurrency operations. Whether you're working with Ethereum Virtual Machine (EVM) based networks, UTXO-based networks like Bitcoin and Litecoin, or TON, AioTx provides a unified and user-friendly interface for interacting with these blockchains.

I created AioTx because I wanted to consolidate all the crypto operations that I frequently use into one convenient package. The goal was to have a collection of crypto clients that I regularly work with, all in one place, with a consistent and intuitive API.

Key Features
------------

1. **EVM Client:** AioTx offers an EVM client that supports popular EVM-based networks such as Ethereum, Binance Smart Chain, Polygon, Avalanche, Fantom, Cronos, and more. With the EVM client, you can easily generate addresses, retrieve balances, send transactions, interact with smart contracts, and perform various other operations.

2. **UTXO Client:** For UTXO-based networks like Bitcoin and Litecoin, AioTx provides a UTXO client. This client allows you to generate addresses, import addresses for monitoring, retrieve balances, estimate fees, and send transactions effortlessly. The UTXO client also includes support for bulk transactions, enabling you to send multiple transactions in a single operation.

3. **TON Client:** Client for Telegram Open Network - now we have monitoring and token sending for it. TON client also includes support for bulk transactions, enabling you to send multiple transactions in a single operation.

4. **TRON Client:** Client for TRON (trx) blockchain - you can monitor transaction and do TRX/TRC20 transactions

5. **Blockchain Monitoring:** One of the standout features of AioTx is its blockchain monitoring capabilities. You can easily monitor new blocks and transactions on the supported blockchains by registering custom handlers. AioTx provides a simple and intuitive way to start and stop monitoring, and it even allows you to monitor multiple clients simultaneously. Integration with the Aiogram library is also supported, enabling you to send notifications or perform actions based on the received blocks and transactions.

6. **Database Storage:** AioTx includes built-in support for database storage, allowing you to store transaction and UTXO data for efficient monitoring and management. You have the flexibility to choose between SQLite and MySQL as the database backend, both of which have been thoroughly tested and are known to work seamlessly with AioTx.

7. **Testing:** To ensure the reliability and stability of AioTx, the package is extensively covered by tests. The test suite includes comprehensive test cases for various scenarios, networks, and operations. AioTx utilizes the VCR (Video Cassette Recorder) library to record and replay network interactions, making the tests deterministic and independent of external services.

Getting Node Url
----------------

For testing purposes, you can use public nodes, but for production, it's better to get a private or at least a shared node. You can obtain one for free on platforms like `Get Block <https://account.getblock.io/sign-in?ref=NWUzNjUzNjktY2EzMy01YzI3LWFlZDUtZjYzYmM1OWU0NmFk>`_ or `Quick Node <https://www.quicknode.com/?via=aiotx>`_

By using these referral URLs, you'll be supporting the project, and I would greatly appreciate your contribution.

Installing
----------

Some clients need sub-dependencies, and if you want to use only TON, for example, you may not need sub-dependencies for BTC/ETH. Because of that, they are divided into extras.

To be able to use TON, please use:

```python
pip install aiotx
```

To be able to use BTC/LTC (UTXO), please use:

```python
pip install aiotx[utxo]
```

To be able to use ETH/MATIC/BSC/TRON (EVM), please use:

```python
pip install aiotx[evm]
```

or for all of them:

```python
pip install aiotx[utxo,evm]
```


Getting Started
---------------

To start using AioTx, simply install the package using pip:

.. code-block:: python

   pip install aiotx


Once installed, you can import the desired client and start interacting with the respective blockchain. Here's a quick example of how to use the EVM client:

Sending Bulk Transactions (Bitcoin):

.. code-block:: python

   from aiotx.clients import AioTxBTCClient

   async def main():
      btc_client = AioTxBTCClient("NODE_URL")
      
      destinations = {
         "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa": 1000000,
         "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2": 500000
      }
      
      private_key = "YOUR_PRIVATE_KEY"
      txid = await btc_client.send_bulk(private_key, destinations)
      print(f"Transaction ID: {txid}")

   asyncio.run(main())


Sending Tokens (Ethereum):

.. code-block:: python

   from aiotx.clients import AioTxETHClient

   async def main():
      eth_client = AioTxETHClient("NODE_URL")
      
      private_key = "YOUR_PRIVATE_KEY"
      to_address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
      # Example token address (Uniswap)
      token_address = "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"
      amount = eth_client.to_wei(10, "ether")  # Sending 10 tokens
      
      tx_hash = await eth_client.send_token(private_key, to_address, token_address, amount)
      print(f"Transaction Hash: {tx_hash}")

   asyncio.run(main())


.. code-block:: python

   from aiotx.clients import AioTxETHClient

   async def main():
      eth_client = AioTxETHClient("NODE_URL")
      
      private_key = "YOUR_PRIVATE_KEY"
      to_address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
      amount = eth_client.to_wei(0.5, "ether")  # Sending 0.5 ETH
      
      tx_hash = await eth_client.send(private_key, to_address, amount)
      print(f"Transaction Hash: {tx_hash}")

   asyncio.run(main())


Sending Native Currency (Bitcoin):#

.. code-block:: python

   from aiotx.clients import AioTxBTCClient

   async def main():
      btc_client = AioTxBTCClient("NODE_URL")
      
      private_key = "YOUR_PRIVATE_KEY"
      to_address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
      amount = 1000000  # Sending 0.01 BTC (amount is in satoshis)
      
      txid = await btc_client.send(private_key, to_address, amount)
      print(f"Transaction ID: {txid}")

   asyncio.run(main())


Satoshi Conversions:

.. code-block:: python

   from aiotx.clients import AioTxBTCClient

   async def main():
      btc_client = AioTxBTCClient("NODE_URL")
      
      # Converting satoshis to BTC
      satoshis = 1000000
      btc = btc_client.from_satoshi(satoshis)
      print(f"{satoshis} satoshis = {btc} BTC")
      
      # Converting BTC to satoshis
      btc = 0.01
      satoshis = btc_client.to_satoshi(btc)
      print(f"{btc} BTC = {satoshis} satoshis")

   asyncio.run(main())


.. toctree::
   :maxdepth: 100
   :caption: Available Clients:

   clients/evm_client/index
   clients/utxo_client/index
   clients/ton_client/index
   clients/tron_client/index

.. toctree::
   :maxdepth: 100
   :caption: Monitoring:

   monitoring

.. toctree::
   :maxdepth: 100
   :caption: Testing:

   testing

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`