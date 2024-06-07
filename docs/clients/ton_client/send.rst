send
====

.. code-block:: python

    async def send(
        mnemonic: str, 
        to_address: str, 
        amount: int, 
        seqno: int = None,
        memo: str = None
        ) -> str:

Send TON tokens from one address to another on the TON blockchain.

Please note that method will not work on HighloadWalletV2Contract (wallet for bulk send), but it's work fine with any other wallet type (default one as well)


Parameters:

    - **mnemonic** (str): The mnemonic phrase of the sender's wallet.
    - **to_address** (str): The TON blockchain address of the recipient.
    - **amount** (int): The amount of TON tokens to send, in nano grams. Use the `to_nano` method to convert from other units to nano grams.
    - **seqno** (int, optional): The sequence number of the transaction. If not provided, it will be automatically fetched using the `get_transaction_count` method.
    - **memo** (str, optional): Memo for your transaction, empty string by default
    
Returns:

    - **str**: The transaction hash of the sent transaction.

Example usage:

.. code-block:: python

    mnemonic = "your mnemonic phrase here"
    to_address = "EQDvRVnNMFgg8Wc4UZqVb8lnsTrPVwdX0-mYu_SdPzt0dIWX"
    amount = ton_client.to_nano(1.5)  # Convert 1.5 TON to nano grams

    transaction_hash = await ton_client.send(mnemonic, to_address, amount)
    print(f"Transaction sent with hash: {transaction_hash}")

In this example, the `send` method is called with the sender's mnemonic phrase, the recipient's TON blockchain address, and the amount to send in nano grams (converted using the `to_nano` method).

The method first checks if the `amount` is an integer and raises an `AssertionError` if it's not. It then retrieves the network parameters if not already available.

Next, it derives the sender's address from the provided mnemonic phrase using the `get_address_from_mnemonics` method. If the `seqno` parameter is not provided, it automatically fetches the current transaction count for the sender's address using the `get_transaction_count` method.

Note:

    - There might be a minimal amount required for the first send transaction because it deploys the sender's contract (address) and pays for it with the standard transaction fee.
    - If you want to send multiple transactions in bulk, you may need to increment the `seqno` manually to ensure the correct sequence of transactions.
