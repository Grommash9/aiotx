send
================

.. code-block:: python

    async send(private_key: str, to_address: str, amount: int, gas_price: int, gas_limit: int = 21000) -> str

Send a BSC transaction.

Parameters:
    - private_key (str): The private key of the sender.
    - to_address (str): The recipient's BSC address.
    - amount (int): The amount in wei to send.
    - gas_price (int): The gas price in wei.
    - gas_limit (int, optional): The gas limit (default is `21000`).

Returns:
    str: The transaction hash.

Example usage:

.. code-block:: python

    transaction_hash = await bsc_client.send(private_key, "0x1234567890123456789012345678901234567890", 1000000000000000000, 5000000000)