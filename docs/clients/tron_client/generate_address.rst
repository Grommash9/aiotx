generate_address
================

Generate a new address and its corresponding private key.

Returns:

    - **dict**: A dict containing the private key, hex address, base58 address and public key.

Example usage:

.. code-block:: python

    wallet = tron_client.generate_address()

.. code-block:: python

    {
    'base58check_address': 'TRbkuCKpqPCFEnWTExeeuADA4pNF9Mqwfb', 
    'hex_address': '41ab737d3fc5828dcaf7d605477435d6f3fce02392', 
    'private_key': 'c5e6a5b71d109f1879c2fe48a10f31b55c13d0cfe46c80cd55456c823d7be0ec', 
    'public_key': '76a4228aea00e52495339f125dbdb06aebdc50c32f7bd17cd341bef28efb3af1e75de3839a353426858aa8d0cdf6d5b1a8bc0777d737e86e35b4c8d8416bb540'
    }