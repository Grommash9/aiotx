send_bulk
=========

.. code-block:: python

    async def send_bulk(mnemonic: str,
    destinations: list[dict]
    ) -> str:

Send TON tokens to multiple recipients in a single transaction using the HighloadWalletV2Contract.

    **Important:** Before using the `send_bulk` method, you must create and deploy a HighloadWalletV2Contract wallet. The default wallet will not work with this method. Ensure that the wallet has sufficient balance to deploy itself and cover the transaction fees.

Parameters:

    - **mnemonic** (str): The mnemonic phrase of the sender's HighloadWalletV2Contract wallet.
    - **destinations** (list[dict]): A list of dictionaries representing the recipient information. Each dictionary should contain the following keys:
        - **address** (str): The TON blockchain address of the recipient.
        - **amount** (int): The amount of TON tokens to send to the recipient, in nano grams.
        - **payload** (str, optional): The payload (memo) to include with the transaction for the recipient.
        - **send_mode** (int, optional): The send mode for the transaction (default is 1).

Returns:

    - **str**: The transaction hash of the sent bulk transaction.

Example usage:

.. code-block:: python

    from aiotx.utils.tonsdk.contract.wallet import WalletVersionEnum
    from aiotx.clients import AioTxTONClient
    import asyncio

    # Create a TON client with HighloadWalletV2Contract
    bulk_ton_client = AioTxTONClient(
    "https://testnet.toncenter.com/api/v2",
    workchain=0,
    wallet_version=WalletVersionEnum.hv2,
    )
    # Define the list of recipients
    recipients_list = [
    {
    "address": "0QAEhA1CupMp7uMOUfHHoh7sqAMNu1xQOydf8fQf-ATpkbpT",
    "amount": 1,
    "payload": "Hello, recipient 1!",
    "send_mode": 1,
    },
    {
    "address": "UQDlTHD4T79EyT96gkYNKd3iuRd2__6gGh2PCKpU57jSWQ7j",
    "amount": 10,
    "payload": "Hello, recipient 5!",
    "send_mode": 1,
    },
    ]
    # Deploy the HighloadWalletV2Contract wallet (required before sending)
    tx_id = await bulk_ton_client.deploy_wallet("your mnemonic phrase here")
    
    # Send TON tokens to multiple recipients using the send_bulk method
    tx_id = await bulk_ton_client.send_bulk(
        "your mnemonic phrase here",
        recipients_list,
    )
    print("Transaction ID:", tx_id)


In this example, we create a TON client with the HighloadWalletV2Contract wallet version. We define a list of recipients, each with their address, amount to send, payload (memo), and send mode.

Before using the `send_bulk` method, we deploy the HighloadWalletV2Contract wallet using the `deploy_wallet` method and the sender's mnemonic phrase. This step is necessary to ensure the wallet is ready to send transactions.

Finally, we call the `send_bulk` method with the sender's mnemonic phrase and the list of recipients. The method returns the transaction hash of the sent bulk transaction.

Note:

 - Make sure to replace `"your mnemonic phrase here"` with the actual mnemonic phrase of the sender's HighloadWalletV2Contract wallet.
 - Ensure that the wallet has sufficient balance to cover the deployment costs and transaction fees.