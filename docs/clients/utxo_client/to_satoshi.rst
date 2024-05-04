to_satoshi
==========

.. code-block:: python

    to_satoshi(number: Union[int, float, str, decimal.Decimal]) -> int


Convert a value from the specified unit to satoshi.

Parameters:

    - **number** (Union[int, float, str, decimal.Decimal]): The value to convert.

Returns:

    - **int**: The converted value in wei.

Example usage:

.. code-block:: python

    value_in_satoshi = AioTxBTCClient.to_wei(1.5)