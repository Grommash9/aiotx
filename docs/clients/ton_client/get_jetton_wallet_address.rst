get_jetton_wallet_address
=========================

.. code-block:: python

    async def get_jetton_wallet_address(
        address: str,
        jetton_master_address: str
    ) -> str:

Retrieves the Jetton wallet address for a given user address and Jetton master contract address.

Parameters:

    - **address** (str): The user's TON blockchain address.
    - **jetton_master_address** (str): The address of the Jetton master contract.

Returns:

    - **str**: The Jetton wallet address associated with the user's address for the specified Jetton.

Raises:

    - **InvalidAddressError**: If the provided address or jetton_master_address is invalid.
    - **RpcConnectionError**: If there's an issue connecting to the TON RPC.

Example usage:

.. code-block:: python

    user_address = "EQCc39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2e"
    jetton_master_address = "EQAiboDEv_qRrcEdrYdwbVLNOXBHwShFbtKGbQVJ2OKxY_Di"
    
    jetton_wallet_address = await ton_client.get_jetton_wallet_address(
        user_address, 
        jetton_master_address
    )
    print(f"Jetton wallet address: {jetton_wallet_address}")

In this example, we retrieve the Jetton wallet address for a specific user and Jetton master contract. The method returns the Jetton wallet address associated with the user for the specified Jetton.