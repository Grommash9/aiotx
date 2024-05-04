to_wei
======

.. code-block:: python

    to_wei(number: Union[int, float, str, decimal.Decimal], unit: str) -> int


Convert a value from the specified unit to wei.

Parameters:

    - **number** (Union[int, float, str, decimal.Decimal]): The value to convert.
    - **unit** (str): The unit of the value (e.g., "ether", "gwei").

Returns:

    - **int**: The converted value in wei.

Example usage:

.. code-block:: python

    value_in_wei = AioTxBSCClient.to_wei(1.5, "ether")