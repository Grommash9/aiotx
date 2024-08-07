generate_address
================

Create a new wallet and generate its corresponding private key, public key, and address.

Returns:

- **tuple**: A tuple containing the following keys:
    - ``private_key`` (str): The private key of the wallet.
    - ``address`` (str): The address of the wallet.

The wallet is created using a hierarchical deterministic (HD) key derivation path specific to the cryptocurrency (Bitcoin or Litecoin) and network (mainnet or testnet).

The derived keys and address are generated as follows:
- The private key is derived from the HD key using the specified derivation path.
- The hash160 (RIPEMD-160 hash of the SHA-256 hash) of the public key is calculated.
- The address is generated by encoding the hash160 using the bech32 format with the appropriate prefix based on the cryptocurrency and network.

Example usage:

.. code-block:: python

    # Create a Bitcoin client instance for mainnet
    btc_mainnet_client = AioTxBTCClient(
        node_url="https://bitcoin-node-url"
        )

    # Generate a Bitcoin wallet with mainnet bech32 address
    btc_mainnet_wallet = btc_mainnet_client.create_wallet()
    print("Bitcoin mainnet wallet:", btc_mainnet_wallet)

    # Create a Litecoin client instance for testnet
    ltc_testnet_client = AioTxLTCClient(
        node_url="https://litecoin-testnet-node-url", testnet=True
        )

    # Generate a Litecoin wallet with testnet bech32 address
    ltc_testnet_wallet = ltc_testnet_client.create_wallet()
    print("Litecoin testnet wallet:", ltc_testnet_wallet)

Output:

.. code-block:: text

    Litecoin testnet wallet: {
        '7a8872a2cb66f8b2be886db2c43b97b0613dc6749a5de22c6afebff50e688b1c',
        'tltc1q9g5dqfzveq9mku6zefdqfa256pteph8hs5khg2'
    }

Note:
- The ``testnet`` parameter in the client initialization determines whether the wallet is created for the mainnet or testnet.
- The derivation path and wallet prefix are set based on the specific cryptocurrency and network.
  - For Bitcoin mainnet, the derivation path is ``"m/84'/0'/0'/0/0"`` and the prefix is ``'bc'``.
  - For Bitcoin testnet, the derivation path is ``"m/84'/0'/0'/0/0"`` and the prefix is ``'tb'``.
  - For Litecoin mainnet, the derivation path is ``"m/84'/2'/0'/0/0"`` and the prefix is ``'ltc'``.
  - For Litecoin testnet, the derivation path is ``"m/84'/2'/0'/0/0"`` and the prefix is ``'tltc'``.