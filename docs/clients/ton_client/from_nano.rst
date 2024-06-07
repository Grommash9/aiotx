from_nano
=========

.. code-block:: python

    def from_nano(number: int, unit: str = "ton") -> int:

Convert a given amount from nano grams to a specified unit of TON cryptocurrency.

Parameters:

    - **number** (int): The amount in nano grams to be converted.
    - **unit** (str, optional): The target unit to convert the `number` to. Default is "ton". Supported units are:
        - "ton": Convert to TON.
        - "nano": No conversion needed, as the amount is already in nano grams.
        - "micro": Convert to micro TON.
        - "milli": Convert to milli TON.
        - "kiloton": Convert to kilo TON.
        - "megaton": Convert to mega TON.
        - "gigaton": Convert to giga TON.

Returns:

    - **int**: The converted amount in the specified unit.

Raises:

    - **ValueError**: If the provided `number` is not a valid integer or if an unsupported `unit` is specified.

Example usage:


.. code-block:: python

    amount_in_ton = ton_client.from_nano(1500000000, unit="ton")
    print(f"1500000000 nano grams is equal to {amount_in_ton} TON")

In this example, the `from_nano` method is called with an amount of 1500000000 nano grams and the target unit "ton". The method internally uses the `tonsdk_from_nano` function from the TON SDK to perform the unit conversion.

If the conversion is successful, the method returns the converted amount in the specified unit as an integer.
