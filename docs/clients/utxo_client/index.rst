UTXO client
===========

Introduction
------------

The Unspent Transaction Output (**UTXO**) Client is a parent client for UTXO-based cryptocurrencies, including Bitcoin (**BTC**) and Litecoin (**LTC**). These cryptocurrencies share similar logic in many aspects, so they are merged into the same parent client.

The **AioTxBTCClient** and **AioTxLTCClient** are derived classes of **AioTxUTXOClient** and are specifically designed to interact with Bitcoin and Litecoin networks, respectively.

Please note that when reading this documentation, the methods can be used for any UTXO-based cryptocurrency supported by the library.

QuickStart
----------

To create an instance of `AioTxBTCClient` or `AioTxLTCClient`, you need to provide the following parameters:

    - **node_url**: The URL of the node to connect to.
    - **headers** (dict, optional): The list of headers what will be used for interactions with node
    - **testnet** (optional): A boolean indicating whether to use the testnet network (default is `False`).
    - **node_username** (optional): The username for authentication with the node (default is an empty string).
    - **node_password** (optional): The password for authentication with the node (default is an empty string).
    - **db_url** (optional): The URL of the database to store transaction and UTXO data (default is `"sqlite+aiosqlite:///aiotx_utxo.sqlite"`).

.. code-block:: python

    from aiotx.clients import AioTxBTCClient, AioTxLTCClient
    import asyncio

    async def main():
        # Create a Bitcoin client instance for mainnet
        btc_mainnet_client = AioTxBTCClient(
         node_url="https://bitcoin-node-url"
         )

        # Create a Litecoin client instance for testnet
        ltc_testnet_client = AioTxLTCClient(
         node_url="https://litecoin-testnet-node-url", 
         testnet=True
         )
        # Use the client instances to interact with the respective networks
        # ...

    asyncio.run(main())

In this example, we create instances of `AioTxBTCClient` and `AioTxLTCClient` by providing the necessary parameters. The `testnet` parameter is set to `True` for the Litecoin client to indicate that we want to use the testnet.


Important Note
--------------

Please note that the **UTXO client functionality in AioTx heavily relies on a database** to store and manage UTXO data. Without a properly configured database, the UTXO client will not work as intended. The database is essential for monitoring addresses, tracking UTXOs, and preventing double-spending.
SQLite Database (Default)

By default, AioTx uses SQLite as the database backend. AioTx will automatically create and manage the SQLite database file for you.
The SQLite database file will be created in the same directory as your Python script with the name aiotx_utxo.sqlite

Database Storage
----------------

AioTx stores transaction and UTXO data in a database for efficient monitoring and management. You can use either SQLite or MySQL as the database backend. Both options have been tested and are working well.

To use SQLite (default), simply provide the SQLite database URL when creating the client instance:

.. code-block:: python

   btc_client = AioTxBTCClient(
    "https://btc.example.com",
    db_url="sqlite+aiosqlite:///aiotx_utxo.sqlite"
    )

To use MySQL, provide the MySQL database URL:

.. code-block:: python

   btc_client = AioTxBTCClient(
    "https://btc.example.com", 
    db_url="mysql+aiomysql://user:password@localhost/aiotx_utxo"
    )

The client will automatically create the necessary tables in the database to store address, UTXO, and block information.

Database Tables
---------------

AioTx uses the following tables to store UTXO and related data:

+----------------------+--------------------------------------------------------+
| Table Name           | Description                                            |
+======================+========================================================+
| {currency}_addresses | Stores the imported addresses and their associated     |
|                      | block numbers.                                         |
+----------------------+--------------------------------------------------------+
| {currency}_utxo      | Stores the UTXO (Unspent Transaction Output) data,     |
|                      | including transaction ID, output index, address,       |
|                      | amount in satoshis, and whether it has been used.      |
+----------------------+--------------------------------------------------------+
| {currency}_last_block| Stores the last processed block number for each        |
|                      | currency.                                              |
+----------------------+--------------------------------------------------------+

The table names are prefixed with the currency name (e.g., "bitcoin_addresses", "litecoin_utxo") to allow storing data for multiple currencies in the same database.

UTXO Logic
----------

AioTx uses the UTXO (Unspent Transaction Output) model to manage and track the available funds for each address. The UTXO model is used by Bitcoin, Litecoin, and other UTXO-based cryptocurrencies.

When an address is imported using the `import_address` method, AioTx starts monitoring the blockchain for transactions involving that address from the specified block number onwards. It stores the UTXO data in the `{currency}_utxo` table, including the transaction ID, output index, address, amount in satoshis, and whether the UTXO has been spent.

When a new transaction is detected for an imported address, AioTx updates the UTXO table accordingly. If the transaction creates a new UTXO for the address, it is added to the table with the `used` flag set to `False`. If the transaction spends an existing UTXO, the corresponding entry in the table is marked as `used` by setting the `used` flag to `True`.

The `get_balance` method retrieves the balance of an address by summing the amounts of all unused UTXOs associated with that address.

When creating a new transaction using the `send` or `send_bulk` methods, AioTx selects the necessary UTXOs to cover the transaction amount and fee. It marks those UTXOs as used in the database to prevent double-spending.

The `{currency}_last_block` table keeps track of the last processed block number for each currency. This allows AioTx to resume monitoring from the last processed block in case of a restart or interruption. The `monitor` subclass handles the database initialization and performs the necessary database operations.

By utilizing the UTXO model and storing the relevant data in the database, AioTx provides an efficient way to manage and monitor the available funds for each imported address.

Note: The specific implementation details of the UTXO logic may vary depending on the cryptocurrency and the client subclass being used (e.g., `AioTxBTCClient`, `AioTxLTCClient`).


Usage
-----

**You can use that clients for network monitoring.**

To use the UTXO client, you first need to create an instance of the desired client class (`AioTxBTCClient` or `AioTxLTCClient`) by providing the necessary parameters such as the node URL, node username (optional), node password (optional), and testnet flag.

Once you have the client instance, you can use the available methods to interact with the respective cryptocurrency network. These methods may include retrieving block information, generating wallets, sending transactions, and more.

Please refer to the individual method documentations for detailed information on how to use each method provided by the UTXO client classes.


Methods
-------

.. toctree::
   :maxdepth: 10

   
   get_block_by_number
   get_last_block_number
   generate_address
   import_address
   get_address_from_private_key
   get_balance
   from_satoshi
   to_satoshi
   estimate_smart_fee
   send
   send_bulk
   get_tx_fee
   get_raw_transaction
   