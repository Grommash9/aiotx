get_balance
===========

.. code-block:: python

    async get_balance(address, block_parameter: BlockParam = BlockParam.LATEST) -> int


Get the balance of an address at a specific block.

Parameters:
    - **address** (str): The address.
    - **block_parameter** (BlockParam, optional): The block parameter (default is `BlockParam.LATEST`).

Returns:
    - **int**: The balance in wei.

Example usage:

.. code-block:: python

    balance = await eth_client.get_balance(
        "0x1234567890123456789012345678901234567890"
        )