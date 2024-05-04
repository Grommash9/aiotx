get_transaction
===============

.. code-block:: python

    async get_transaction(hash) -> dict


Get the details of a transaction by its hash.

Parameters:
    - hash (str): The transaction hash.

Returns:
    dict: The transaction details, including the decoded input data.

Raises:
    TransactionNotFound: If the transaction is not found.

Example usage:

.. code-block:: python

    transaction = await bsc_client.get_transaction("0x1234567890abcdef...")