get_tx_fee
==========

.. code-block:: python

    await get_tx_fee(tx_id: str) -> int:
    

Retrieves the fee paid for a given transaction.

Parameters:

   - **tx_id** (str): The transaction ID for which to retrieve the fee.

Returns:

   - **int**: The fee paid for the transaction in satoshis.

Raises:

   - **NotImplementedError**: If the transaction is a coinbase (miner) transaction, which is not yet implemented.
   - **ValueError**: If the verbosity level is not one of the allowed values (0, 1, or 2).

Example:

.. code-block:: python

    fee = await btc_client.get_tx_fee(
        "35158b7a8b6057bc67f6d904c64b5986adea8260f0bc96cbd755b530878e3cc2"
        )
    print(fee)
    # Output: 6000
