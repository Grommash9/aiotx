get_address_from_private_key
============================

.. code-block:: python

    get_address_from_private_key(private_key: str)


Get the address corresponding to a private key.

Parameters:
    - **private_key** (str): The private key.

Returns:
    - **str**: The address.

Example usage:

.. code-block:: python

    address = eth_client.get_address_from_private_key(private_key)