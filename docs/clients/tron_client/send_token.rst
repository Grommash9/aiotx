send_token
==========

.. code-block:: python

    async send_token(
        private_key: str,
        to_address: str,
        contract: str,
        amount: int,
        memo: str = None,
    )

Send a TRC20 token transaction on the TRON network.

Parameters:

    - **private_key** (str): The private key of the sender.
    - **to_address** (str): The recipient's TRON address.
    - **contract** (str): The TRC20 token contract address.
    - **amount** (int): The amount of tokens to send.
    - **memo** (str, optional): The memo or extra data to include in the transaction. If provided, it should be a string.

Returns:

    - **str**: The transaction hash.

Raises:

    - **TypeError**: When the `memo` parameter is not a string.
    - **CreateTransactionError**: When there is an error creating the transaction, such as insufficient balance or an invalid token contract address.
    - **ValueError**: When an invalid private key is provided. The private key should be a valid TRON private key.

Example usage:

.. code-block:: python

    # Sending 10 tokens (assuming 6 decimals)
    sun_amount = tron_client.to_sun(10)
    transaction_hash = await tron_client.send_token(
        "private_key", "to_address", "contract_address", 
        sun_amount, "Example memo"
    )

In this example, a TRC20 token transaction is sent on the TRON network using the provided private key (`private_key`) to the specified destination address (`to_address`). The `contract` parameter specifies the address of the TRC20 token contract. The amount of tokens to be sent is calculated by converting the desired amount to SUN using the `to_sun` method, assuming the token has 6 decimal places. An optional memo can be included in the transaction.

The `send_token` method internally calls the `_create_trc20_transfer_transaction` method to create the transaction details. It then signs the transaction using the private key and broadcasts the signed transaction to the TRON network using the `broadcast_transaction` method.

If the transaction is successful, the method returns the transaction hash as a string.

Note: The `send_token` method assumes that the connected TRON node has sufficient funds to cover the transaction cost. If there is insufficient balance or any other error occurs during the transaction creation or broadcasting, the appropriate exception will be raised.

The `_create_trc20_transfer_transaction` method is an internal method used by the `send_token` method to create the TRC20 token transfer transaction details. It constructs the transaction payload, including the sender and recipient addresses, the token contract address, the amount, and any optional memo. It then makes an API call to the TRON network to create the transaction.

The test cases provided cover various scenarios, such as sending tokens with different amounts and memos, handling invalid inputs, and checking for the expected transaction hash. The tests use the `vcr` library to record and replay network requests, ensuring consistent behavior during testing.