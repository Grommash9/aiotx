send_token
==========

.. code-block:: python

    async send_token(
        private_key: str, to_address: str, 
        token_address: str, amount: int, 
        nonce: int = None, gas_price: int = None, 
        gas_limit: int = 100000
        ) -> str

Send a token transaction.

Parameters:

    - **private_key** (str): The private key of the sender.

    - **to_address** (str): The recipient's address.

    - **token_address** (str): The token contract address.

    - **amount** (int): The amount of tokens to send.

    - **nonce** (int, optional): The nonce of the transaction. If not provided, it will be automatically fetched.

    - **gas_price** (int, optional): The gas price in wei. If not provided, it will be automatically fetched.
    
    - **gas_limit** (int, optional): The gas limit (default is `100000`).

Returns:
    - **str**: The transaction hash.

Raises:

    - **WrongPrivateKey**: When an invalid private key is provided. The private key should be a valid Ethereum private key.

    - **ValueError**: When an invalid Ethereum address is provided as the recipient (`to_address`). The address should be a valid Ethereum address.

    - **ReplacementTransactionUnderpriced**: When the specified gas price is too low compared to the current gas price on the Ethereum network. It indicates that the transaction is not competitive enough to be included in a block.

    - **AioTxError**: When there is an issue with the transaction parameters, such as when the gas limit is set to zero or when there is insufficient balance to cover the transaction cost.

    - **InvalidArgumentError**: When an invalid argument is passed to a method, such as an invalid contract address.

    - **TypeError**: When an invalid type is passed as an argument to a method, such as an invalid contract address (non-string type).

    - **NonceTooLowError** (implied): When the specified nonce is lower than the current nonce of the sender's address. It indicates that the transaction is trying to use a nonce that has already been used.

Note: Some errors, such as `ReplacementTransactionUnderpriced` and `NonceTooLowError`, may be raised due to the test cases reusing the same VCR (Video Cassette Recorder) data for every nonce request, which suggests that the test cases are not fully isolated and may have dependencies on the recorded VCR data.

Example usage:

.. code-block:: python

    # Sending 1 USDT (6 decimals)
    wei_amount = eth_client.to_wei(1, "mwei")
    transaction_hash = await eth_client.send_token(
        "private_key", "to_address", "contract_address", wei_amount
        )

In the `send_token` method, some parameters are optional:

- **nonce**: If not provided, the nonce will be automatically fetched using the `get_transactions_count` method with the `BlockParam.PENDING` parameter.
- **gas_price**: If not provided, the gas price will be automatically fetched using the `get_gas_price` method.
- **gas_limit**: If not provided, the gas limit will set to `100000`

By making these parameters optional, it provides more flexibility and convenience when sending token transactions.

Here's an example of sending two token transactions in quick succession using custom nonces:

.. code-block:: python


    wei_amount = eth_client.to_wei(1, "mwei")
    nonce = await eth_client.get_transactions_count("sender_address")
    
    first_tx = await eth_client.send_token(
        "private_key", "to_address", "contract_address", 
        wei_amount, nonce=nonce)
    assert isinstance(first_tx, str)
    
    second_tx = await eth_client.send_token(
        "private_key", "sender_address", "contract_address", 
        wei_amount, nonce=nonce + 1)
    assert isinstance(second_tx, str)

In this example, we first fetch the current nonce of the sender's address using `get_transactions_count`. Then, we send the first token transaction using the obtained nonce. For the second transaction, we increment the nonce by 1 to ensure that it is sent immediately after the first transaction.

By specifying the nonce manually, we can send multiple transactions in quick succession without waiting for the previous transaction to be mined.

Note: Make sure to handle the case where the specified nonce is lower than the current nonce of the sender's address, as it may result in the transaction being rejected by the network.