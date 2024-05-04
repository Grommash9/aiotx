## AioTx

AioTx is an asynchronous library for interacting with various cryptocurrencies and blockchains. It aims to provide a lightweight and efficient solution for developers to integrate cryptocurrency functionalities into their projects without relying on heavy dependencies like web3.js or bitcoin-lib.
Features

- Asynchronous and non-blocking design for high performance
- Support for multiple cryptocurrencies and blockchains
- Minimal dependencies to keep the library small and fast
- Easy-to-use API for common tasks like wallet creation, balance retrieval, and transaction signing
- Extensible architecture for adding support for new cryptocurrencies and blockchains

# Installation
You can install AioTx using pip:
```
pip install aiotx
```

# Usage
Here's a simple example of how to use AioTx to create a wallet and retrieve its balance:

```
from aiotx import AioTxBSCClient

bsc_client = AioTxBSCClient(node_url="https://example.com", chain_id=97)

async def main():
    # Create a new wallet
    address, private_key = bsc_client.generate_address()
    
    # Retrieve the wallet balance
    balance = await bsc_client.get_balance(address)
    print(f"Wallet balance: {balance}")

    # Send BNB
    tx_id = await bsc_client.send(private_key, to_address, amount)
    print(f"Your tx: {tx_id}")

    # Send any token
    tx_id = await bsc_client.send_token(private_key, to_address, contract_address, amount)
    print(f"Your tx: {tx_id}")

# Run the async main function
asyncio.run(main())
```

For more detailed usage examples and API reference, please refer to the documentation.

https://grommash9.github.io/aiotx/

# Contributing
Contributions to AioTx are welcome! If you find any bugs, have feature requests, or want to contribute improvements, please open an issue or submit a pull request on the GitHub repository.

# License
AioTx is open-source software licensed under the MIT License.