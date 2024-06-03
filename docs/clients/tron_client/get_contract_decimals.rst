get_contract_decimals
=====================

.. code-block:: python

    async get_contract_decimals(contract_address: str) -> int

Retrieves the number of decimals for a given contract address.

Parameters:

    - **contract_address** (str): The address of the contract.

Returns:

    - **int**: The number of decimals for the contract.

Example usage:

.. code-block:: python

    contract_address = "TXLAQ63Xg1NAzckPwKHvzw7CSEmLMEqcdj"

    decimals = await tron_client.get_contract_decimals(contract_address)

    print(f"The contract {contract_address} has {decimals} decimals.")


Under the hood, this method works by encoding the decimals() function signature and hashing it using the keccak hash function. The first 8 characters of the hash result are used as the method ID. The method then makes an RPC call to the Ethereum node using the eth_call method, passing the contract address and the method ID as parameters. The result is returned as a hexadecimal string, which is converted to an integer representing the number of decimals for the contract. If the result is "0x", the method returns 0 as the number of decimals.