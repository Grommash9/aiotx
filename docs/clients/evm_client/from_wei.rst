from_wei
========

.. code-block:: python

    from_wei(
        number: Union[int, str], 
        unit: str = "ether"
        ) -> Union[int, decimal.Decimal]

Convert a value in wei to its equivalent in the specified unit.

Parameters:

    - **number** (Union[int, str]): The value in wei. If a string is provided, it will be interpreted as a hexadecimal number if it starts with "0x" or "0X" and contains only valid hexadecimal digits.

    - **unit** (str, optional): The unit to convert to (e.g., "ether", "gwei"). Default value - "ether".

Returns:

    - Union[int, decimal.Decimal]: The converted value.

Example usage:

.. code-block:: python

    value_in_ether = eth_client.from_wei(1000000000000000000, "ether")
    value_in_ether = eth_client.from_wei("0x38d7ea4c68000", "ether")
