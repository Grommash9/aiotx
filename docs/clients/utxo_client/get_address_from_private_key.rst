get_address_from_private_key
============================

.. code-block:: python

   def get_address_from_private_key(private_key: str) -> dict

Parameters:
   - **private_key** (str): Private key to derive the address from.

Returns:
   - **dict**: A dictionary containing the private key, public key, and address.

The `get_address_from_private_key` function retrieves the address associated with the given private key. It returns a dictionary containing the following keys:

   - "private_key": The input private key.
   - "public_key": The public key derived from the private key.
   - "address": The Bitcoin address associated with the private key.

Example usage:

.. code-block:: python

   private_key = "7a8872a2cb66f8b2be886db2c43b97b0613dc6749a5de22c6afebff50e688b1c"
   address_data = btc_client.get_address_from_private_key(private_key)
   address = address_data["address"]
   print(address)

Output:
   tltc1q9g5dqfzveq9mku6zefdqfa256pteph8hs5khg2

Real Data Example:

.. code-block:: python

    # Generate a new address
    private_key, address = asyncio.run(ltc_client.generate_address())
    print("Private Key:", private_key)
    print("Address:", address)

    # Get address data from the private key
    address_data = ltc_client.get_address_from_private_key(private_key)
    print("Address Data:", address_data)

    Output:
    Private Key: 7a8872a2cb66f8b2be886db2c43b97b0613dc6749a5de22c6afebff50e688b1c
    Address: tltc1q9g5dqfzveq9mku6zefdqfa256pteph8hs5khg2
    Address Data: {
        'private_key': '7a8872a2cb66f8b2be886db2c43b97b0613dc6749a5de22c6afebff50e688b1c',
        'public_key': '02741fae22d2bc4debcc51540f4c7668ff85d9758071057716b94845e09d171eca',
        'address': 'tltc1q9g5dqfzveq9mku6zefdqfa256pteph8hs5khg2'
    }

In this real data example:

1. We first generate a new Litecoin address using the `generate_address` function of the `ltc_client` object. This function returns the private key and the corresponding address.

2. We print the generated private key and address.

3. We then call the `get_address_from_private_key` function, passing the generated private key as an argument. This function returns a dictionary containing the private key, public key, and address associated with the private key.

4. Finally, we print the address data dictionary returned by the `get_address_from_private_key` function.

The output shows the generated private key, address, and the address data dictionary containing the private key, public key, and address. This demonstrates the usage of the `get_address_from_private_key` function with a real private key and the corresponding address data it returns.