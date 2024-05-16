get_balance
===========

.. code-block:: python

    async def get_balance(address: str) -> int:

Retrieves the balance of a given Bitcoin address.

Parameters:
    - **address** (str): The Bitcoin address for which to retrieve the balance.

Returns:
    - int: The balance of the address in satoshis.

The ``get_balance`` method retrieves the balance of a specified Bitcoin address by fetching the UTXO (Unspent Transaction Output) data associated with that address from the wallet monitoring system.

It performs the following steps:

1. Calls the ``_get_utxo_data`` method of the ``monitor`` object to retrieve the UTXO data for the given address.
2. If the retrieved UTXO data is empty (i.e., there are no UTXOs associated with the address), it returns 0 as the balance.
3. If there are UTXOs associated with the address, it calculates the total balance by summing the ``amount_satoshi`` attribute of each UTXO.
4. Returns the total balance in satoshis.

Example usage:

.. code-block:: python

    # Retrieve the balance of an address
    balance = await wallet.get_balance("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
    print(f"Balance: {balance} satoshis")

In this example, the balance of the address "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa" is retrieved using the ``get_balance`` method. The balance is returned in satoshis.

Note: The ``get_balance`` method relies on the wallet monitoring system to have the UTXO data for the specified address. Make sure to import the address using the ``import_address`` method before retrieving its balance.
