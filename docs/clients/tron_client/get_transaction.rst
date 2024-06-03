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

    transaction = await tron_client.get_transaction("0xbee7c8234683d0835878b7ee04094af486593d5a1042f060a17e35e5fe9a5b22")
    print("tx_data", transaction)

Output:

.. code-block:: python

    tx_data {'blockHash': '0x0000000002d3228b5189c60781b3ef1aa64382fae5f715649052305ab093f230', 
    'blockNumber': '0x2d3228b', 'from': '0xd3682962027e721c5247a9faf7865fe4a71d5438', 
    'gas': '0x3476', 'gasPrice': '0x1a4', 
    'hash': '0xbee7c8234683d0835878b7ee04094af486593d5a1042f060a17e35e5fe9a5b22', 
    'input': '0xa9059cbb000000000000000000000000e2b1a24707701dd1d1bc72d18aef7ca9dfa75'
    '45d0000000000000000000000000000000000000000000000000000000ba43b7400', 
    'nonce': '0x0000000000000000', 'r': 
    '0x7e45be012ff71220265ee93722841d808ece23c53b5043e59f013393de5cd79b', 
    's': '0x1da7dc2a635b32647038cff56464fe2e9951f743ee1cd5955c31a6082f3fa0eb', 
    'to': '0xea51342dabbb928ae1e576bd39eff8aaf070a8c6', 
    'transactionIndex': '0x0', 'type': '0x0', 'v': '0x1b', 'value': '0x0', 
    'aiotx_decoded_input': {'function_name': 'transfer', 
    'parameters': {'_to': '0xe2b1a24707701dd1d1bc72d18aef7ca9dfa7545d', 
    '_value': 50000000000}}}

The `get_transaction` method retrieves the details of a transaction using its hash. It returns a dictionary containing the transaction details, including the decoded input data if available.

The `aiotx_decoded_input` field in the returned transaction dictionary contains the decoded input data, which provides information about the function call and its parameters.

**Note:** The addresses in the returned transaction data are in hexadecimal format. If you need to convert the addresses to Base58 format, you can use the `hex_address_to_base58` function:

.. code-block:: python

    tron_client = AioTxTRONClient("NODE_URL")
    # Example usage
    base58_address = tron_client.hex_address_to_base58("0xd3682962027e721c5247a9faf7865fe4a71d5438")
    print(base58_address)

    Output: TVF2Mp9QY7FEGTnr3DBpFLobA6jguHyMvi

The `hex_address_to_base58` function takes a hexadecimal address as input and converts it to Base58 format using the `tronpy` library. If the input address starts with the "0x" prefix, it replace it by 41. If the input is not a valid hexadecimal address, it raises a `TypeError` exception.