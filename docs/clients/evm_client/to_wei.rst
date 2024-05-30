to_wei
======

.. code-block:: python

    to_wei(
        number: Union[int, float, str, decimal.Decimal], 
        unit: str = "ether"
        ) -> int

Convert a value from the specified unit to wei.

Parameters:

    - **number** (Union[int, float, str, decimal.Decimal]): The value to convert. If a string is provided, it will be interpreted as a hexadecimal number if it starts with "0x" or "0X" and contains only valid hexadecimal digits. Otherwise, it will be interpreted as a floating-point number.

    - **unit** (str, optional): The unit of the value (e.g., "ether", "gwei"). Default value - "ether".

Returns:

    - **int**: The converted value in wei.

Example usage:

.. code-block:: python

    value_in_wei = AioTxBSCClient.to_wei(1.5, "ether")
    value_in_wei = AioTxBSCClient.to_wei("0x38d7ea4c68000", "ether")

Raises:

- **ValueError**: If the input string cannot be interpreted as a valid number.