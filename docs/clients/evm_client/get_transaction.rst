get_transaction
===============

.. code-block:: python

    async get_transaction(hash: str) -> dict


Get the details of a transaction by its hash.


Parameters:

    - **hash** (str): The transaction hash.

Returns:

    - **dict**: The transaction details, including the decoded input data if available.

Raises:

    - **TransactionNotFound**: If the transaction is not found.

Example usage:

.. code-block:: python

    transaction = await bsc_client.get_transaction("0x1234567890abcdef...")


The **get_transaction** method retrieves the details of a transaction using its hash. It returns a dictionary containing the transaction details, including the decoded input data if available.

The **aiotx_decoded_input** field in the returned transaction dictionary contains the decoded input data, which provides information about the function call and its parameters. However, it's important to note that the decoding process relies on the ABI (Application Binary Interface) entries defined in the client. If the transaction's input data matches a known function signature, the method will decode the input data and provide the function name and parameters. Otherwise, if the input data represents a custom contract call or a function signature not defined in the client's ABI, the **aiotx_decoded_input** field will be set to a dictionary with `'function_name'` and `'parameters'` keys, both having a value of `None`.

Here are a few examples of decoded input data for different scenarios:

1. Example of a transfer transaction on the Binance Smart Chain (BEP20 token):

.. code-block:: python

    transaction = await bsc_client.get_transaction("0x1234567890abcdef...")
    print(transaction["aiotx_decoded_input"])

    # Output:
    {
        'function_name': 'transfer',
        'parameters': {'recipient': '0x1234567890123456789012345678901234567890', 'amount': 100}
    }


In this example, the transaction's input data represents a **transfer** function call on a BEP20 token contract. The decoded input data provides the recipient address and the amount being transferred.

2. Example of a transfer transaction on the Ethereum network (ERC20 token):

.. code-block:: python

    transaction = await eth_client.get_transaction("0x0987654321abcdef...")
    print(transaction["aiotx_decoded_input"])

    # Output:
    {
        'function_name': 'transfer',
        'parameters': {'_to': '0x0987654321098765432109876543210987654321', '_value': 1000}
    }


In this example, the transaction's input data represents a **transfer** function call on an ERC20 token contract. The decoded input data provides the recipient address (named `_to`) and the amount being transferred (named `_value`).

3. Example of a custom contract call that cannot be decoded:

.. code-block:: python

    transaction = await bsc_client.get_transaction("0xabcdef1234567890...")
    print(transaction["aiotx_decoded_input"])

    # Output:
    {
        'function_name': None,
        'parameters': None
    }


In this example, the transaction's input data represents a custom contract call that is not defined in the client's ABI. As a result, the **aiotx_decoded_input** field is set to a dictionary with **'function_name'** and **'parameters'** keys, both having a value of **None**.

It's important to keep in mind that the decoding process depends on the available ABI entries in the client. If the transaction's input data does not match any known function signature, the decoding will not be possible, and the **aiotx_decoded_input** field will be set to a dictionary with `None` values for the function name and parameters.