from_satoshi
============

.. code-block:: python

    from_satoshi(number: int) -> Union[int, decimal.Decimal]

Convert a value in satoshi to it BTC/LTC amount.

Parameters:
    - **number** (int): The value in wei.

Returns:
    - Union[int, decimal.Decimal]: The converted value.

Example usage:

.. code-block:: python

    value_in_btc = eth_client.from_satoshi(1000000000000000000)