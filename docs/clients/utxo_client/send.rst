send
====

.. code-block:: python

    async def send(
        private_key: str,
        to_address: str,
        amount: int,
        total_fee: Optional[int],
        fee_per_byte: Optional[int],
        conf_target: int = 6,
        estimate_mode: FeeEstimate = FeeEstimate.CONSERVATIVE,
        deduct_fee: bool = False
    ) -> str:

Send a transaction on the Bitcoin network.

Parameters:

    - **private_key** (str): The private key of the sender.
    - **to_address** (str): The recipient's Bitcoin address.
    - **amount** (int): The amount in satoshis to send.
    - **total_fee** (Optional[int]): The total transaction fee in satoshis. If provided, this fee will be used for the transaction. If not provided, the fee will be automatically estimated based on the ``fee_per_byte`` or the ``conf_target`` and ``estimate_mode``.
    - **fee_per_byte** (Optional[int]): The fee per byte in satoshis. If provided, this value will be used to calculate the transaction fee based on the transaction size. If not provided, the fee will be estimated based on the ``conf_target`` and ``estimate_mode``.
    - **conf_target** (int, optional): The confirmation target, which represents the number of blocks within which the transaction should be confirmed. Default is 6 blocks.
    - **estimate_mode** (FeeEstimate, optional): The fee estimation mode. It can be one of the following values:
        - ``FeeEstimate.UNSET``: No specific fee estimation mode is set.
        - ``FeeEstimate.ECONOMICAL``: Economical fee estimation mode, which aims to minimize the transaction fee.
        - ``FeeEstimate.CONSERVATIVE`` (default): Conservative fee estimation mode, which aims to ensure faster confirmation by using a higher fee.
    - **deduct_fee** (bool, optional): Indicates whether the transaction fee should be deducted from the sent amount. Default is ``False``.

Returns:

    - **str**: The transaction ID (TXID) of the sent transaction.

Raises:

    - **WrongPrivateKey**: When an invalid private key is provided. The private key should be a valid Bitcoin private key.
    - **ValueError**: When an invalid Bitcoin address is provided as the recipient (``to_address``). The address should be a valid Bitcoin address.
    - **InsufficientFunds**: When there are insufficient funds (UTXOs) available in the sender's wallet to cover the transaction amount and fee. This error occurs when the wallet does not have enough spendable UTXOs to construct the transaction.
    - **NoUTXOsFound**: When there are no UTXOs (Unspent Transaction Outputs) found for the sender's address. This error occurs when the wallet monitoring process has not detected any spendable UTXOs associated with the sender's address in the database.

Code Examples:

1. Sending a transaction with a custom total fee:

.. code-block:: python

    tx_id = await ltc_public_client.send(
        "your_private_key",
        "recipient_address",
        amount=1000000,  # 0.01 LTC
        total_fee=5000   # 0.00005 LTC
    )

In this example, a transaction is sent with a custom total fee of 5,000 satoshis (0.00005 LTC). The provided total fee will be used for the transaction, regardless of the transaction size.

2. Sending a transaction with a custom fee per byte:

.. code-block:: python

    tx_id = await ltc_public_client.send(
        "your_private_key",
        "recipient_address",
        amount=1000000,  # 0.01 LTC
        fee_per_byte=10  # 10 satoshis per byte
    )

Here, a custom fee per byte of 10 satoshis is specified. The actual transaction fee will be calculated based on the transaction size and the provided fee per byte value.

3. Sending a transaction with the fee deducted from the sent amount:

.. code-block:: python

    tx_id = await ltc_public_client.send(
        "your_private_key",
        "recipient_address",
        amount=1000000,
        deduct_fee=True
    )

In this example, the `deduct_fee` parameter is set to `True`, indicating that the transaction fee should be deducted from the sent amount. The recipient will receive an amount slightly less than the specified `amount`, as the fee will be subtracted from it.

When calling the `send` method with different parameters, the following actions will be performed:
    - The provided private key will be used to sign the transaction.
    - The specified recipient address will receive the sent amount.
    - If a custom total fee is provided using the `total_fee` parameter, it will be used for the transaction.
    - If a custom fee per byte is provided using the `fee_per_byte` parameter, the transaction fee will be calculated based on the transaction size and the fee per byte value.
    - If neither `total_fee` nor `fee_per_byte` is provided, the fee will be estimated based on the `conf_target` and `estimate_mode`.
    - If `deduct_fee` is set to `True`, the transaction fee will be deducted from the sent amount.
    - The transaction will be broadcast to the Litecoin network, and the transaction ID (TXID) will be returned.
