get_last_block
==============

.. code-block:: python

    async get_last_block() -> int


Get the number of the latest block on the blockchain.

Returns:

    - **int**: The latest block number.

Example usage:

.. code-block:: python

    latest_block = await bsc_client.get_last_block()