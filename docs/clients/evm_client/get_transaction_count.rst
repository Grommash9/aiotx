get_transaction_count
=====================

.. code-block:: python

    async get_transaction_count(address, block_parameter: BlockParam = BlockParam.LATEST) -> int


Get the number of transactions sent from an address at a specific block.

Parameters:

    - **address** (str): The address.
    - **block_parameter** (BlockParam, optional): The block parameter (default is `BlockParam.LATEST`).

Returns:

    - **int**: The transaction count.

Example usage:

.. code-block:: python

    transaction_count = await eth_client.get_transaction_count(
        "0x1234567890123456789012345678901234567890"
        )