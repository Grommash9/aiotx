get_contract_balance
====================

.. code-block:: python

    async get_contract_balance(
        address, contract_address, 
        block_parameter: BlockParam = BlockParam.LATEST
        ) -> int



Get the token balance of an address for a specific token contract at a specific block.

Parameters:

    - **address** (str): The address.
    - **contract_address** (str): The token contract address.
    - **block_parameter** (BlockParam, optional): The block parameter (default is `BlockParam.LATEST`).

Returns:

    - **int**: The token balance.

Example usage:

.. code-block:: python

    token_balance = await eth_client.get_contract_balance(
        "0x1234567890123456789012345678901234567890", 
        "0x0123456789012345678901234567890123456789")