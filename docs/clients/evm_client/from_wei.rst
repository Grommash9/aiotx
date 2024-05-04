from_wei
========

.. code-block:: python

    from_wei(number: int, unit: str) -> Union[int, decimal.Decimal]

Convert a value in wei to its equivalent in the specified unit.

Parameters:
    - **number** (int): The value in wei.
    - **unit** (str): The unit to convert to (e.g., "ether", "gwei").

Returns:
    - Union[int, decimal.Decimal]: The converted value.

Example usage:

.. code-block:: python

    value_in_ether = eth_client.from_wei(1000000000000000000, "ether")