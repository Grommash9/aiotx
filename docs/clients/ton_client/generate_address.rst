generate_address
================

Create a new wallet and generate its corresponding private key, user-friendly url-safe address and raw address.
You will need raw address for transaction monitoring and it's better to save it, but you will always be able to get it later.

Returns:

- **tuple**: A tuple containing the following:

    - ``mnemonics`` (str): The str of wallet mnemonics (private key).
    - ``address`` (str): The user-friendly url-safe address, can share it with users.
    - ``raw_address`` (str): The raw address of the wallet we will need that format for monitoring.

Example usage:

.. code-block:: python

    from aiotx.clients import AioTxTONClient


    ton_client = AioTxTONClient(
        node_url="https://ton-node-url"
        )

    memo, address, raw_address = await ton_client.generate_address()
    print(memo)
    print(address)
    print(raw_address)

Output:

.. code-block:: text

    fault toilet valid lazy morning home select field future warm notice utility now laundry doctor galaxy indoor message roof develop baby mammal long minute 0:eb233d106e452fdf542538f91fcd544521d911f4c050d8942d31d734e5bd81b9
    UQDrIz0QbkUv31QlOPkfzVRFIdkR9MBQ2JQtMdc05b2BuQdh
    0:eb233d106e452fdf542538f91fcd544521d911f4c050d8942d31d734e5bd81b9
