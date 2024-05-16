import_address
==============

.. code-block:: python

    async def import_address(
        address: str, 
        block_number: int = None
        ):


Import an address into the wallet monitoring system.

The ``import_address`` method allows you to import a Bitcoin address into the wallet monitoring system. This is particularly useful in cases where you have lost the database containing the UTXO (Unspent Transaction Output) information and need to resync the wallet data from a specific block.

When importing an address, you can optionally specify the block number from which to start syncing the address. If the block number is not provided, it will default to the last known block in the wallet.

Importing an address is also necessary when you want to retrieve the UTXOs associated with an address. In order to query the UTXOs for an address, it must first be imported into the wallet monitoring system. Once an address is imported, the wallet will start tracking its transactions and UTXOs from the specified block onwards.

Parameters:
    - **address** (str): The Bitcoin address to import.
    - **block_number** (int, optional): The block number from which to start syncing the address. If not provided, it will default to the last known block in the wallet.

The ``import_address`` method performs the following steps:

1. Retrieves the last known block number from the wallet.
2. If the ``block_number`` parameter is not provided, it defaults to the last known block number.
3. Adds the provided ``address`` and ``block_number`` to the wallet monitoring system.
4. If the provided ``block_number`` is less than the last known block number in the wallet, it updates the last known block number to ensure consistency.

By importing an address with a specific block number, you can instruct the wallet monitoring system to start syncing the address data from that particular block onwards. This is useful in scenarios where you need to recover the wallet data from a certain point in time, such as when you have lost the UTXO database and want to resync the address data from a known block.

Example usage:

.. code-block:: python

    # Import an address starting from block 100000
    await btc_client.import_address(
        "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", 
        block_number=100000
        )

In this example, the address "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa" is imported into the wallet monitoring system, and the syncing process will start from block 100000 onwards. The wallet will retrieve all the transactions and UTXOs associated with the address from that block and update its internal state accordingly.

To retrieve the UTXOs for an address, you need to import the address first using the ``import_address`` method. After importing the address, you can use the appropriate method provided by the wallet to fetch the UTXOs associated with that address.

Note: Importing an address with a specific block number is particularly useful when you have lost the UTXO database and need to resync the wallet data from a known point. By specifying the block number, you can avoid syncing the entire blockchain and instead start from a specific block, saving time and resources during the syncing process. Additionally, importing an address is a prerequisite for retrieving its UTXOs, as the wallet needs to be aware of the address and track its transactions to determine the available UTXOs.