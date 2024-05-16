get_block_by_number
===================

.. code-block:: python

   async def get_block_by_number(
    block_number: int, 
    verbosity: int = 1
    ) -> dict

Retrieves the block data for the specified block number.

Parameters:
   - **block_number** (int): The block number for which to retrieve the block data.
   - **verbosity** (int, optional): The verbosity level of the block data. Default is 1. Possible values are:
     
     - 0: Returns only the block hash.
     - 1: Returns the block data with transaction hashes instead of full transaction details.
     - 2: Returns the block data with full transaction details.

Returns:
   - dict: A dictionary containing the block data. The structure of the dictionary depends on the verbosity level.

Raises:
   - **BlockNotFound**: If the specified block number does not exist.
   - **ValueError**: If the verbosity level is not one of the allowed values (0, 1, or 2).

Example usage:

.. code-block:: python

   # Retrieve block data with transaction hashes (verbosity level 1)
   block_data = await btc_client.get_block_by_number(
    700000
    )

   # Retrieve block data with full transaction details (verbosity level 2)
   block_data_full = await btc_client.get_block_by_number(
    700000, 
    verbosity=2
    )

The `get_block_by_number` method allows you to retrieve the block data for a specific block number. You can control the level of detail in the returned block data using the `verbosity` parameter.

When `verbosity` is set to 0, only the block hash is returned. When `verbosity` is set to 1 (default), the block data is returned with transaction hashes instead of full transaction details. When `verbosity` is set to 2, the block data is returned with full transaction details.

If the specified block number does not exist, a `BlockNotFound` exception is raised. If an invalid verbosity level is provided, a `ValueError` is raised.

Note: The structure of the returned block data dictionary varies depending on the verbosity level. Make sure to handle the block data appropriately based on the chosen verbosity level.