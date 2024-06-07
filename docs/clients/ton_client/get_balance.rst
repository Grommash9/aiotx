get_balance
===========

.. code-block:: python

    async def get_balance(address) -> int:

Retrieve the balance of a given address on the TON (The Open Network) blockchain.

Parameters:

    - **address** (str): The TON blockchain address for which to retrieve the balance.

Returns:

    - **int**: The balance of the specified address in nano grams (the smallest unit of TON cryptocurrency).

Raises:

    - **InvalidAddress**: If the provided `address` is not a valid TON blockchain address.
    - **AioTxError**: If there is an error while making the RPC call to the TON node.

Example usage:

.. code-block:: python

    balance = await ton_client.get_balance(
        "EQDvRVnNMFgg8Wc4UZqVb8lnsTrPVwdX0-mYu_SdPzt0dIWX"
        )
    print(f"Balance: {balance} nano grams")

In this example, the `get_balance` method is called with a TON blockchain address. It constructs an RPC payload with the "getAddressBalance" method and the provided address as a parameter. The method then sends the RPC request to the connected TON node using the `_make_rpc_call` method.

If the RPC call is successful, the method extracts the balance information from the response and returns it as an integer representing the balance in nano grams.
