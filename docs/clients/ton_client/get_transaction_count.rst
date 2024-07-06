get_transaction_count
=====================

Get the current transaction count (seqno) for a given address.

.. code-block:: python
    
    def get_transaction_count(
        address
        ) -> int

Parameters:

    - **address** (str): The TON address for which to retrieve the transaction count.

Returns:

    - **str**: The current transaction count (seqno) for the given address.


This function retrieves the current transaction count, also known as seqno (sequence number),
for a given TON address. The transaction count is used to ensure that transactions from
the same address are processed in the correct order.

The function first calls the `get_wallet_information` method to obtain the wallet information
for the specified address. Then, it retrieves the `seqno` value from the wallet information
dictionary. If the `seqno` key is not present, it returns 0 as the default transaction count.

This function is automatically called by the `send` method when the `seqno` parameter is not provided.
