send
====

.. code-block:: python

    async send(
        private_key: str, to_address: str, 
        amount: int, nonce: int = None, 
        gas_price: int = None, gas_limit: int = 21000
        ) -> str

Send a transaction on the Ethereum network.

Parameters:

    - **private_key** (str): The private key of the sender.

    - **to_address** (str): The recipient's Ethereum address.

    - **amount** (int): The amount in wei to send.

    - **nonce** (int, optional): The nonce of the transaction. If not provided, it will be automatically fetched.

    - **gas_price** (int, optional): The gas price in wei. If not provided, it will be automatically fetched.

    - **gas_limit** (int, optional): The gas limit (default is `21000`).


Returns:

    - **str**: The transaction hash.

Raises:

    - **WrongPrivateKey**: When an invalid private key is provided. The private key should be a valid Ethereum private key.
    
    - **ValueError**: When an invalid Ethereum address is provided as the recipient (`to_address`). The address should be a valid Ethereum address.
    
    - **ReplacementTransactionUnderpriced**: When the specified gas price is too low compared to the current gas price on the Ethereum network. It indicates that the transaction is not competitive enough to be included in a block.
    
    - **AioTxError**: When there is an issue with the transaction parameters, such as when the gas limit is set to zero or when there is insufficient balance to cover the transaction cost.
    
    - **NonceTooLowError**: When the specified nonce is lower than the current nonce of the sender's address. It indicates that the transaction is trying to use a nonce that has already been used.

Example usage:

.. code-block:: python

    # Sending 0.5 ETH
    amount_in_wei = eth_client.to_wei(0.5)

    transaction_hash = await eth_client.send(
        "private_key", "to_address", 
        amount_in_wei
        )

In this example, a transaction is sent on the Ethereum network using the provided private key (`private_key`) to the specified destination address (`to_address`). The amount to be sent is 0.5 ether, and the gas price is set to 5 Gwei (5 * 10^9 wei).

The `send` method automatically fetches the current nonce and gas price if they are not provided. It constructs the transaction object, signs it with the private key, and sends it to the Ethereum network using the `eth_sendRawTransaction` RPC method.

If the transaction is successful, the method returns the transaction hash as a string.

Note: The `send` method assumes that the connected Ethereum node has sufficient funds to cover the transaction cost. If there is insufficient balance, an `AioTxError` will be raised.