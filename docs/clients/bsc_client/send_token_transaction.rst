send_token_transaction
======================

.. code-block:: python

    async send_token_transaction(private_key: str, to_address: str, token_address: str, amount: int, gas_price: int, gas_limit: int = 100000) -> str

Send a token transaction.

Parameters:
    - private_key (str): The private key of the sender.
    - to_address (str): The recipient's BSC address.
    - token_address (str): The token contract address.
    - amount (int): The amount of tokens to send.
    - gas_price (int): The gas price in wei.
    - gas_limit (int, optional): The gas limit (default is `100000`).

Returns:
    str: The transaction hash.

Example usage:

.. code-block:: python

    transaction_hash = await bsc_client.send_token_transaction(private_key, "0x1234567890123456789012345678901234567890", "0x0123456789012345678901234567890123456789", 1000000000000000000, 5000000000)