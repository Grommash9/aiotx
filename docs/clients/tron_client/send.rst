send
====

.. code-block:: python

    async send(
        private_key: str,
        to_address: str,
        amount: int,
        memo: str = None,
    ) -> str

Send a transaction on the TRON network.

Parameters:

    - **private_key** (str): The private key of the sender.
    - **to_address** (str): The recipient's TRON address.
    - **amount** (int): The amount in SUN to send.
    - **memo** (str, optional): The memo or extra data to include in the transaction. If provided, it should be a string.

Returns:

    - **str**: The transaction hash.

Raises:

    - **TypeError**: When the `memo` parameter is not a string.
    - **CreateTransactionError**: When there is an error creating the transaction, such as insufficient balance or invalid recipient address.
    - **ValueError**: When an invalid private key is provided. The private key should be a valid TRON private key.

Example usage:

.. code-block:: python

    # Sending 10 TRX with a memo
    amount_in_sun = tron_client.to_sun(10)
    transaction_hash = await tron_client.send(
        "private_key", "to_address",
        amount_in_sun, "Example memo"
    )

In this example, a transaction is sent on the TRON network using the provided private key (`private_key`) to the specified destination address (`to_address`). The amount to be sent is 10 TRX, which is converted to SUN using the `to_sun` method. An optional memo can be included in the transaction.

The `send` method internally calls the `_create_transaction` method to create the transaction details. It then signs the transaction using the private key and broadcasts the signed transaction to the TRON network using the `broadcast_transaction` method.

If the transaction is successful, the method returns the transaction hash as a string.

Note: The `send` method assumes that the connected TRON node has sufficient funds to cover the transaction cost. If there is insufficient balance or any other error occurs during the transaction creation or broadcasting, the appropriate exception will be raised.

The `_create_transaction` method is an internal method used by the `send` method to create the transaction details. It communicates with the TRON API to generate the transaction payload, including the sender and recipient addresses, the amount, and any optional memo.

The test cases provided cover various scenarios, such as sending TRX with different amounts and memos, handling invalid inputs, and checking for the expected transaction hash. The tests use the `vcr` library to record and replay network requests, ensuring consistent behavior during testing.