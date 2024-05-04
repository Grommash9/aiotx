UTXO client
===========

Introduction
------------

The Unspent Transaction Output (**UTXO**) Client is a parent client for UTXO-based cryptocurrencies, including Bitcoin (**BTC**) and Litecoin (**LTC**). These cryptocurrencies share similar logic in many aspects, so they are merged into the same parent client.

The **AioTxBTCClient** and **AioTxLTCClient** are derived classes of **AioTxUTXOClient** and are specifically designed to interact with Bitcoin and Litecoin networks, respectively.

Please note that when reading this documentation, the methods can be used for any UTXO-based cryptocurrency supported by the library.

QuickStart
----------

To create an instance of **AioTxBTCClient** or **AioTxLTCClient**, you need to provide the node URL, node username (optional), node password (optional), and specify whether to use the testnet or mainnet. Here's an example:

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

Class Hierarchy
---------------

The UTXO client classes follow a hierarchical structure:

- `AioTxUTXOClient`: The base class for UTXO-based clients. It provides common functionality and abstractions for interacting with UTXO-based cryptocurrencies.

  - `AioTxBTCClient`: A derived class specifically for interacting with the Bitcoin network. It inherits from `AioTxUTXOClient` and sets the appropriate derivation path and wallet prefix based on the network (mainnet or testnet).

  - `AioTxLTCClient`: A derived class specifically for interacting with the Litecoin network. It also inherits from `AioTxUTXOClient` and sets the appropriate derivation path and wallet prefix based on the network (mainnet or testnet).


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

   from_satoshi
   to_satoshi