get_block_by_number
===================

.. code-block:: python

    async get_block_by_number(block_number: int, transaction_detail_flag: bool = True)


Get a block by its block number.

Parameters:
    - **block_number** (int): The block number.
    - **transaction_detail_flag** (bool, optional): Whether to include transaction details in the response (default is `True`).

Returns:
    - **dict**: The block details.

Example usage:

.. code-block:: python

    block = await eth_client.get_block_by_number(1000000)