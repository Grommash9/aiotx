send
====

.. code-block:: python

    async def send(
        private_key: str,
        to_address: str,
        amount: int,
        fee: int = None,
        conf_target: int = 6,
        estimate_mode: FeeEstimate = FeeEstimate.CONSERVATIVE,
        deduct_fee: bool = False
    ) -> str:

Send a transaction on the Bitcoin network.

Parameters:
    - **private_key** (str): The private key of the sender.
    - **to_address** (str): The recipient's Bitcoin address.
    - **amount** (int): The amount in satoshis to send.
    - **fee** (int, optional): The transaction fee in satoshis. If not provided, it will be automatically estimated based on the ``conf_target`` and ``estimate_mode``.
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

The ``send`` method internally calls the ``_build_and_send_transaction`` method to construct and send the transaction.

The ``_build_and_send_transaction`` method performs the following steps:

1. Retrieves the sender's address from the provided private key using the ``get_address_from_private_key`` method.
2. Fetches the UTXO data for the sender's address from the database using the ``_get_utxo_data`` method of the monitor object.
3. If the fee is not provided, it estimates the fee by creating an empty transaction, estimating the fee rate based on the ``conf_target`` and ``estimate_mode``, signing the empty transaction, estimating its size, and calculating the fee.
4. Creates the actual transaction using the ``create_transaction`` method, specifying the destinations, UTXOs, sender's address, fee, and whether to deduct the fee from the sent amount.
5. Signs the transaction using the ``sign_transaction`` method with the provided private key(s).
6. Sends the signed transaction to the Bitcoin network using the ``send_transaction`` method.
7. Marks the used inputs (UTXOs) as spent in the database using the ``_mark_inputs_as_used`` method.
8. Returns the transaction ID (TXID) of the sent transaction.

The ``sign_transaction`` method signs the transaction using the provided private key(s) for each input.

The ``_mark_inputs_as_used`` method marks the used inputs (UTXOs) as spent in the database to prevent double-spending.

The ``send_transaction`` method sends the raw transaction to the Bitcoin network using the ``sendrawtransaction`` RPC method.

The ``FeeEstimate`` enum defines the available fee estimation modes: ``UNSET``, ``ECONOMICAL``, and ``CONSERVATIVE``.