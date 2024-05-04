BSC client
==========

Introduction
------------

AioTxBSCClient is a Python client library for interacting with the Binance Smart Chain (BSC) blockchain using asynchronous programming. It provides a simple and intuitive way to perform various operations such as querying account balances, sending transactions, and monitoring block and transaction events.

Creating an Instance
--------------------

To create an instance of AioTxBSCClient, you need to provide the BSC node URL and the chain ID. Here's an example:

.. code-block:: python

   from aiotx.clients import AioTxBSCClient

   node_url = "https://bsc-dataseed.binance.org/"
   chain_id = 56

   bsc_client = AioTxBSCClient(node_url, chain_id)

Methods
-------


.. toctree::
   :maxdepth: 1

   from_wei 
   generate_address 
   get_address_from_private_key 
   get_balance 
   get_block_by_number 
   get_gas_price 
   get_last_block 
   get_token_balance 
   get_transaction_count 
   get_transaction 
   send_token_transaction 
   send_transaction to_wei