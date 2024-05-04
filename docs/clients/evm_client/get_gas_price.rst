get_gas_price
=============

.. code-block:: python

    async get_gas_price() -> int


Get the current gas price on the network.

Returns:

   - **int**: The gas price in wei.

Example usage:

.. code-block:: python

    gas_price = await bsc_client.get_gas_price()