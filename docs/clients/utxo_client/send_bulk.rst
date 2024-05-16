send_bulk
=========

.. code-block:: python

    async def send_bulk(
        private_key: str,
        destinations: dict[str, int],
        fee: int = None,
        conf_target: int = 6,
        estimate_mode: FeeEstimate = FeeEstimate.CONSERVATIVE,
        deduct_fee: bool = False
    ) -> str:

Send a bulk transaction on the Bitcoin network.

The ``send_bulk`` method is similar to the ``send`` method, but it allows sending a transaction to multiple recipients in a single transaction. The main difference is that instead of accepting a single recipient address and amount, it accepts a dictionary of recipient addresses and their corresponding amounts.

Parameters:
    - **private_key** (str): The private key of the sender.
    - **destinations** (dict[str, int]): A dictionary where the keys are the recipient Bitcoin addresses and the values are the amounts in satoshis to send to each address.
    - **fee** (int, optional): The transaction fee in satoshis. If not provided, it will be automatically estimated based on the ``conf_target`` and ``estimate_mode``.
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

Note: The ``send_bulk`` method is useful for scenarios where you need to send transactions to multiple recipients efficiently, as it combines multiple outputs into a single transaction, reducing the overall transaction fees compared to sending individual transactions to each recipient.