to_nano
=======

.. code-block:: python

    def to_nano(
        number: Union[int, float, str, decimal.Decimal], 
        unit: str = "ton"
        ) -> int:

Convert a given amount from a specified unit to nano grams, the smallest unit of TON cryptocurrency.

Parameters:

    - **number** (Union[int, float, str, decimal.Decimal]): The amount to be converted to nano grams. It can be an integer, float, string, or decimal.Decimal.
    - **unit** (str, optional): The unit of the `number` parameter. Default is "ton". Supported units are:
        - "ton": The amount is in TON.
        - "nano": The amount is already in nano grams.
        - "micro": The amount is in micro TON.
        - "milli": The amount is in milli TON.
        - "kiloton": The amount is in kilo TON.
        - "megaton": The amount is in mega TON.
        - "gigaton": The amount is in giga TON.

Returns:

    - **int**: The converted amount in nano grams.

Raises:

    - **ValueError**: If the provided `number` is not a valid numeric value or if an unsupported `unit` is specified.

Example usage:

.. code-block:: python

    amount_in_nano = ton_client.to_nano(1.5, unit="ton")
    print(f"1.5 TON is equal to {amount_in_nano} nano grams")

In this example, the `to_nano` method is called with an amount of 1.5 and the unit "ton". The method internally uses the `tonsdk_to_nano` function from the TON SDK to perform the unit conversion.

If the conversion is successful, the method returns the converted amount in nano grams as an integer.
