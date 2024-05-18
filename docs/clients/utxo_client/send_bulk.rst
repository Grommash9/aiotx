send_bulk
=========

.. code-block:: python

    async def send_bulk(
        private_key: str,
        destinations: dict[str, int],
        total_fee: Optional[int],
        fee_per_byte: Optional[int],
        conf_target: int = 6,
        estimate_mode: FeeEstimate = FeeEstimate.CONSERVATIVE,
        deduct_fee: bool = False
    ) -> str:

Send a bulk transaction on the Bitcoin network.

The ``send_bulk`` method is similar to the ``send`` method, but it allows sending a transaction to multiple recipients in a single transaction. The main difference is that instead of accepting a single recipient address and amount, it accepts a dictionary of recipient addresses and their corresponding amounts.

Parameters:

    - **private_key** (str): The private key of the sender.
    - **destinations** (dict[str, int]): A dictionary where the keys are the recipient Bitcoin addresses and the values are the amounts in satoshis to send to each address.
    - **total_fee** (Optional[int]): The total transaction fee in satoshis. If provided, this fee will be used for the transaction. If not provided, the fee will be automatically estimated based on the ``fee_per_byte`` or the ``conf_target`` and ``estimate_mode``.
    - **fee_per_byte** (Optional[int]): The fee per byte in satoshis. If provided, this value will be used to calculate the transaction fee based on the transaction size. If not provided, the fee will be estimated based on the ``conf_target`` and ``estimate_mode``.
    - **conf_target** (int, optional): The confirmation target, which represents the number of blocks within which the transaction should be confirmed. Default is 6 blocks.
    - **estimate_mode** (FeeEstimate, optional): The fee estimation mode. It can be one of the following values:
        - ``FeeEstimate.UNSET``: No specific fee estimation mode is set.
        - ``FeeEstimate.ECONOMICAL``: Economical fee estimation mode, which aims to minimize the transaction fee.
        - ``FeeEstimate.CONSERVATIVE`` (default): Conservative fee estimation mode, which aims to ensure faster confirmation by using a higher fee.
    - **deduct_fee** (bool, optional): Indicates whether the transaction fee should be deducted from the sent amounts. If set to ``True``, the fee will be deducted evenly from all recipients' amounts. Default is ``False``.

Returns:

    - **str**: The transaction ID (TXID) of the sent bulk transaction.

The ``send_bulk`` method internally calls the ``_build_and_send_transaction`` method to construct and send the transaction, passing the ``destinations`` dictionary instead of a single recipient address and amount.

The logic for constructing and sending the transaction is the same as in the ``send`` method, with the following differences:
- The ``destinations`` parameter is a dictionary of recipient addresses and amounts, allowing for sending to multiple recipients in a single transaction.
- If the ``deduct_fee`` parameter is set to ``True``, the transaction fee will be deducted evenly from all recipients' amounts. This means that each recipient will receive slightly less than the specified amount, as the fee is distributed among all recipients.

Raises:

    - **WrongPrivateKey**: When an invalid private key is provided. The private key should be a valid Bitcoin private key.
    - **ValueError**: When an invalid Bitcoin address is provided as a recipient address in the ``destinations`` dictionary. All addresses should be valid Bitcoin addresses.
    - **InsufficientFunds**: When there are insufficient funds (UTXOs) available in the sender's wallet to cover the total transaction amount and fee. This error occurs when the wallet does not have enough spendable UTXOs to construct the transaction.
    - **NoUTXOsFound**: When there are no UTXOs (Unspent Transaction Outputs) found for the sender's address. This error occurs when the wallet monitoring process has not detected any spendable UTXOs associated with the sender's address in the database.

Code Examples:

1. Sending a bulk transaction with a custom total fee:

.. code-block:: python

    destinations = {
        "recipient_address_1": 1000000,  # 0.01 LTC
        "recipient_address_2": 500000,   # 0.005 LTC
        "recipient_address_3": 750000    # 0.0075 LTC
    }
    tx_id = await ltc_public_client.send_bulk(
        "your_private_key",
        destinations,
        total_fee=10000  # 0.0001 LTC
    )

In this example, a bulk transaction is sent to multiple recipients with a custom total fee of 10,000 satoshis (0.0001 LTC). The provided total fee will be used for the transaction, regardless of the transaction size.

2. Sending a bulk transaction with a custom fee per byte:

.. code-block:: python

    destinations = {
        "recipient_address_1": 1000000,  # 0.01 LTC
        "recipient_address_2": 500000,   # 0.005 LTC
        "recipient_address_3": 750000    # 0.0075 LTC
    }
    tx_id = await ltc_public_client.send_bulk(
        "your_private_key",
        destinations,
        fee_per_byte=10  # 10 satoshis per byte
    )

Here, a custom fee per byte of 10 satoshis is specified. The actual transaction fee will be calculated based on the transaction size and the provided fee per byte value.

3. Sending a bulk transaction with the fee deducted from the sent amounts:

.. code-block:: python

    destinations = {
        "recipient_address_1": 1000000,  # 0.01 LTC
        "recipient_address_2": 500000,   # 0.005 LTC
        "recipient_address_3": 750000    # 0.0075 LTC
    }
    tx_id = await ltc_public_client.send_bulk(
        "your_private_key",
        destinations,
        deduct_fee=True
    )

In this example, the `deduct_fee` parameter is set to `True`, indicating that the transaction fee should be deducted evenly from all recipients' amounts. Each recipient will receive slightly less than the specified amount, as the fee is distributed among all recipients.

When calling the `send_bulk` method with different parameters, the following actions will be performed:
    - The provided private key will be used to sign the transaction.
    - The specified recipient addresses and amounts from the `destinations` dictionary will be used to construct the transaction outputs.
    - If a custom total fee is provided using the `total_fee` parameter, it will be used for the transaction.
    - If a custom fee per byte is provided using the `fee_per_byte` parameter, the transaction fee will be calculated based on the transaction size and the fee per byte value.
    - If neither `total_fee` nor `fee_per_byte` is provided, the fee will be estimated based on the `conf_target` and `estimate_mode`.
    - If `deduct_fee` is set to `True`, the transaction fee will be deducted evenly from all recipients' amounts.
    - The transaction will be broadcast to the Litecoin network, and the transaction ID (TXID) will be returned.

Note: The `send_bulk` method is useful for scenarios where you need to send transactions to multiple recipients efficiently, as it combines multiple outputs into a single transaction, reducing the overall transaction fees compared to sending individual transactions to each recipient.

Please note that the examples assume you have a `ltc_public_client` instance properly configured with network and connection settings.