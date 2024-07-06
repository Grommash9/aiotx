## AioTx

[![PyPI Downloads](https://img.shields.io/pypi/dm/aiotx.svg)](https://pypistats.org/packages/aiotx)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-ff69b4.svg)](https://github.com/charliermarsh/ruff)
[![Python Versions](https://img.shields.io/pypi/pyversions/aiotx.svg)](https://pypi.org/project/aiotx/)
[![OS Support](https://img.shields.io/badge/OS-Windows%20%7C%20macOS%20%7C%20Linux-blue.svg)](https://pypi.org/project/aiotx/)

[![Bitcoin](https://img.shields.io/badge/Bitcoin-BTC-orange.svg)](https://bitcoin.org/)
[![Litecoin](https://img.shields.io/badge/Litecoin-LTC-lightgrey.svg)](https://litecoin.org/)
[![Ethereum](https://img.shields.io/badge/Ethereum-ETH-blue.svg)](https://ethereum.org/)
[![Binance Smart Chain](https://img.shields.io/badge/Binance%20Smart%20Chain-BSC-yellow.svg)](https://www.binance.org/en/smartChain)
[![Polygon](https://img.shields.io/badge/Polygon-MATIC-purple.svg)](https://polygon.technology/)
[![TON](https://img.shields.io/badge/TON-TON-blue.svg)](https://ton.org/)
[![TRON](https://img.shields.io/badge/TRON-TRX-red.svg)](https://tron.network/)

[![MySQL Test](https://github.com/Grommash9/aiotx/actions/workflows/mysql_test.yml/badge.svg)](https://github.com/Grommash9/aiotx/actions/workflows/mysql_test.yml)
[![Test](https://github.com/Grommash9/aiotx/actions/workflows/test.yml/badge.svg)](https://github.com/Grommash9/aiotx/actions/workflows/test.yml)
[![Ruff lint check](https://github.com/Grommash9/aiotx/actions/workflows/lint-check.yml/badge.svg)](https://github.com/Grommash9/aiotx/actions/workflows/lint-check.yml)

AioTx is a comprehensive Python package designed to simplify and streamline your cryptocurrency operations. Whether you're working with Ethereum Virtual Machine (EVM) based networks, UTXO-based networks like Bitcoin and Litecoin, or TON, AioTx provides a unified and user-friendly interface for interacting with these blockchains.

I created AioTx because I wanted to consolidate all the crypto operations that I frequently use into one convenient package. The goal was to have a collection of crypto clients that I regularly work with, all in one place, with a consistent and intuitive API.

Join telegram channel and chat for updates and help
https://t.me/aiotx_python
https://t.me/aiotx_python_chat

Key Features
------------

1. **EVM Client:** AioTx offers an EVM client that supports popular EVM-based networks such as Ethereum, Binance Smart Chain, Polygon, Avalanche, Fantom, Cronos, and more. With the EVM client, you can easily generate addresses, retrieve balances, send transactions, interact with smart contracts, and perform various other operations.

2. **UTXO Client:** For UTXO-based networks like Bitcoin and Litecoin, AioTx provides a UTXO client. This client allows you to generate addresses, import addresses for monitoring, retrieve balances, estimate fees, and send transactions effortlessly. The UTXO client also includes support for bulk transactions, enabling you to send multiple transactions in a single operation.

3. **TON Client:** Client for Telegram Open Network - now we have monitoring and token sending TON and bulk send, also sending jettons and checking jetton balance

4. **TRON Client:** Client for TRON (trx) blockchain - you can monitor transaction and do TRX/TRC20 transactions

5. **Blockchain Monitoring:** One of the standout features of AioTx is its blockchain monitoring capabilities. You can easily monitor new blocks and transactions on the supported blockchains by registering custom handlers. AioTx provides a simple and intuitive way to start and stop monitoring, and it even allows you to monitor multiple clients simultaneously. Integration with the Aiogram library is also supported, enabling you to send notifications or perform actions based on the received blocks and transactions.

6. **Database Storage:** AioTx includes built-in support for database storage, allowing you to store transaction and UTXO data for efficient monitoring and management. You have the flexibility to choose between SQLite and MySQL as the database backend, both of which have been thoroughly tested and are known to work seamlessly with AioTx.

7. **Testing:** To ensure the reliability and stability of AioTx, the package is extensively covered by tests. The test suite includes comprehensive test cases for various scenarios, networks, and operations. AioTx utilizes the VCR (Video Cassette Recorder) library to record and replay network interactions, making the tests deterministic and independent of external services.

Getting Node Url
----------------

For testing purposes, you can use public nodes, but for production, it's better to get a private or at least a shared node. You can obtain one for free on platforms like [Get Block](https://account.getblock.io/sign-in?ref=NWUzNjUzNjktY2EzMy01YzI3LWFlZDUtZjYzYmM1OWU0NmFk) or [Quick Node](https://www.quicknode.com/?via=aiotx)

By using these referral URLs, you'll be supporting the project, and I would greatly appreciate your contribution.


Getting Started
---------------

To start using AioTx, simply install the package using pip:

There is a high chance what on Ubuntu or other Linux OS you will need to install libgmp that before start:
```
sudo apt-get install libgmp-dev
```


Some clients need sub-dependencies, and if you want to use only TON, for example, you may not need sub-dependencies for BTC/ETH. Because of that, they are divided into extras.

To be able to use TON, please use:

```python
pip install aiotx
```

To be able to use BTC/LTC (UTXO), please use:

```python
pip install aiotx[utxo]
```

To be able to use ETH/MATIC/BSC/TRON (EVM), please use:

```python
pip install aiotx[evm]
```

or for all of them:

```python
pip install aiotx[utxo,evm]
```

Once installed, you can import the desired client and start interacting with the respective blockchain. Here's a quick example of how to use the EVM client:

Sending Bulk Transactions (Bitcoin):
```python
from aiotx.clients import AioTxBTCClient

async def main():
    btc_client = AioTxBTCClient("NODE_URL")
    
    destinations = {
        "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa": 1000000,
        "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2": 500000
    }
    
    private_key = "YOUR_PRIVATE_KEY"
    txid = await btc_client.send_bulk(private_key, destinations)
    print(f"Transaction ID: {txid}")

asyncio.run(main())
```

Sending Tokens (Ethereum):
```python
from aiotx.clients import AioTxETHClient

async def main():
    eth_client = AioTxETHClient("NODE_URL")
    
    private_key = "YOUR_PRIVATE_KEY"
    to_address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
    token_address = "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"  # Example token address (Uniswap)
    amount = eth_client.to_wei(10, "ether")  # Sending 10 tokens
    
    tx_hash = await eth_client.send_token(private_key, to_address, token_address, amount)
    print(f"Transaction Hash: {tx_hash}")

asyncio.run(main())
```

Sending TON (for bulk please check [/examples](https://github.com/Grommash9/aiotx/tree/main/examples)):
```python
    from aiotx.clients import AioTxTONClient
    import asyncio

    ton_client = AioTxTONClient("https://testnet.toncenter.com/api/v2", workchain=0)
    # We are adding workchain here because testnet.toncenter working bad and identify itself as -1 but it should be 0
    # If you are using any other provider it should work fine without workchain param

    amount = ton_client.to_nano(0.0001)
    mnemonic_str = "post web slim candy example glimpse other reduce layer way ordinary hidden dwarf marble fancy gym client soul speed enforce drift huge upset oblige"

    balance = asyncio.run(ton_client.get_balance("UQDU1hdX6SeHmrvzvyjIrLEWUAdJUJar2sw8haIuT_5n-FLh"))

    tx_id = asyncio.run(ton_client.send(mnemonic_str, "0QAEhA1CupMp7uMOUfHHoh7sqAMNu1xQOydf8fQf-ATpkbpT", amount))
    print(tx_id)

    
```
Transferring Jettons:

```python

    from aiotx.clients import AioTxTONClient
    import asyncio

    ton_client = AioTxTONClient("https://testnet.toncenter.com/api/v2", workchain=0)

    mnemonic_str = "your wallet mnemonic phrase here"
    recipient_address = "EQCc39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2e"
    jetton_master_address = "EQAiboDEv_qRrcEdrYdwbVLNOXBHwShFbtKGbQVJ2OKxY_Di"
    amount = 1000000000  # 1 Jetton (assuming 9 decimal places)
    memo = "Payment for services"

    tx_hash = asyncio.run(ton_client.transfer_jettons(
        mnemonic_str,
        recipient_address,
        jetton_master_address,
        amount,
        memo
    ))
    print(f"Jetton transfer transaction hash: {tx_hash}")
    
```

Sending Native Currency (Ethereum):
```python
from aiotx.clients import AioTxETHClient

async def main():
    eth_client = AioTxETHClient("NODE_URL")
    
    private_key = "YOUR_PRIVATE_KEY"
    to_address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
    amount = eth_client.to_wei(0.5, "ether")  # Sending 0.5 ETH
    
    tx_hash = await eth_client.send(private_key, to_address, amount)
    print(f"Transaction Hash: {tx_hash}")

asyncio.run(main())
```

Sending Native Currency (Bitcoin):
```python
from aiotx.clients import AioTxBTCClient

async def main():
    btc_client = AioTxBTCClient("NODE_URL")
    
    private_key = "YOUR_PRIVATE_KEY"
    to_address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    amount = 1000000  # Sending 0.01 BTC (amount is in satoshis)
    
    txid = await btc_client.send(private_key, to_address, amount)
    print(f"Transaction ID: {txid}")

asyncio.run(main())
```

Satoshi Conversions:
```python
from aiotx.clients import AioTxBTCClient

async def main():
    btc_client = AioTxBTCClient("NODE_URL")
    
    # Converting satoshis to BTC
    satoshis = 1000000
    btc = btc_client.from_satoshi(satoshis)
    print(f"{satoshis} satoshis = {btc} BTC")
    
    # Converting BTC to satoshis
    btc = 0.01
    satoshis = btc_client.to_satoshi(btc)
    print(f"{btc} BTC = {satoshis} satoshis")

asyncio.run(main())
```

These examples showcase the simplicity and flexibility of using AioTx for various cryptocurrency operations. Whether you're sending bulk transactions, sending tokens, sending native currency, or converting between different units, AioTx provides a consistent and intuitive API for interacting with different blockchains.


For more detailed usage instructions and examples, please refer to the documentation for each client and feature.

I hope you find AioTx helpful and enjoy using it for your crypto operations. If you have any questions, feedback, or suggestions, please don't hesitate to reach out. Happy coding!

For more detailed usage examples and API reference, please refer to the documentation.

https://grommash9.github.io/aiotx/

# Contributing
Contributions to AioTx are welcome! If you find any bugs, have feature requests, or want to contribute improvements, please open an issue or submit a pull request on the GitHub repository.

# License
AioTx is open-source software licensed under the MIT License.
