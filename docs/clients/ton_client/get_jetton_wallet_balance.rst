get_jetton_wallet_balance
=========================

.. code-block:: python

    async def get_jetton_wallet_balance(
        address: str,
        jetton_master_address: str
    ) -> int:

Retrieves the balance of a specific Jetton for a given user address.

Parameters:

    - **address** (str): The user's TON blockchain address.
    - **jetton_master_address** (str): The address of the Jetton master contract.

Returns:

    - **int**: The balance of the specified Jetton for the given user address, in the smallest units of the Jetton.

Raises:

    - **InvalidAddressError**: If the provided address or jetton_master_address is invalid.
    - **RpcConnectionError**: If there's an issue connecting to the TON RPC.
    - **ValueError**: If the returned data structure is unexpected.

Example usage:

.. code-block:: python

    user_address = "EQCc39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2e"
    jetton_master_address = "EQAiboDEv_qRrcEdrYdwbVLNOXBHwShFbtKGbQVJ2OKxY_Di"
    
    balance = await ton_client.get_jetton_wallet_balance(
        user_address, 
        jetton_master_address
    )
    print(f"Jetton balance: {balance}")

In this example, we retrieve the balance of a specific Jetton for a given user address. The method returns the balance in the smallest units of the Jetton (similar to how TON balances are represented in nanotons).

Note:
    - The returned balance is in the smallest units of the Jetton. To convert it to a more human-readable format, you may need to divide it by 10^9 (assuming 9 decimal places, which is common but not guaranteed for all Jettons).
    - This method first retrieves the Jetton wallet address using `get_jetton_wallet_address`, then queries the balance of that wallet.