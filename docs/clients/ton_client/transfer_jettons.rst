transfer_jettons
================

.. code-block:: python

    async def transfer_jettons(
        self,
        mnemonic: str,
        to_address: str,
        jetton_master_address: str,
        amount: int,
        memo: str = None,
        seqno: int = None,
        fee_amount: int = None
    ) -> str:

Transfers Jettons from the sender's wallet to a specified recipient address.

Parameters:

    - **mnemonic** (str): The mnemonic phrase for the sender's wallet.
    - **to_address** (str): The recipient's TON blockchain address.
    - **jetton_master_address** (str): The address of the Jetton master contract.
    - **amount** (int): The amount of Jettons to transfer, in the smallest units of the Jetton.
    - **memo** (str, optional): An optional comment to attach to the transfer.
    - **seqno** (int, optional): The sequence number for the transaction. If not provided, it will be retrieved automatically.
    - **fee_amount** (int, optional): The amount of TON to attach for fees. If not provided, a default of 0.05 TON will be used.

Returns:

    - **str**: The transaction hash of the transfer operation.

Raises:

    - **InvalidAddressError**: If the provided to_address or jetton_master_address is invalid.
    - **RpcConnectionError**: If there's an issue connecting to the TON RPC.
    - **ValueError**: If the amount is not a positive integer.

Example usage:

.. code-block:: python

    mnemonic = "your wallet mnemonic phrase here"
    recipient_address = "EQCc39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2e"
    jetton_master_address = "EQAiboDEv_qRrcEdrYdwbVLNOXBHwShFbtKGbQVJ2OKxY_Di"
    amount = 1000000000  # 1 Jetton (assuming 9 decimal places)
    memo = "Payment for services"

    tx_hash = await ton_client.transfer_jettons(
        mnemonic,
        recipient_address,
        jetton_master_address,
        amount,
        memo
    )
    print(f"Transfer transaction hash: {tx_hash}")

In this example, we transfer 1 Jetton (assuming 9 decimal places) to the specified recipient address. The method returns the transaction hash of the transfer operation.

Notes:

    - The amount should be specified in the smallest units of the Jetton (similar to how TON amounts are specified in nanotons).
    - The fee_amount is in nanotons. If not specified, a default of 0.05 TON (50,000,000 nanotons) will be used.
    - This method constructs and sends the necessary messages to perform the Jetton transfer according to the TON Jetton standard.
    - Ensure you have sufficient balance of both the Jetton and TON (for fees) in the sender's wallet before initiating the transfer.
