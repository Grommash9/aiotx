get_balance
===========

.. code-block:: python

    async get_balance(address, block_parameter: BlockParam = BlockParam.LATEST) -> int


Get the balance of an address at a specific block.

Parameters:

    - **address** (str): The address.
    - **block_parameter** (BlockParam, optional): The block parameter (default is `BlockParam.LATEST`).

Returns:

    - **int**: The balance in sun.

Example usage:

.. code-block:: python

    balance = await tron_client.get_balance(
        "TEZQQ5BXq3nFKUFJknoV15CW24twzH81La"
        )