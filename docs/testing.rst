Testing AioTx Clients
=====================

AioTx provides comprehensive test suites for its Ethereum (ETH) and Binance Smart Chain (BSC) clients to ensure the reliability and correctness of the implemented methods. The tests cover various scenarios and edge cases to validate the behavior of the clients.

Test Coverage
-------------

The test suites cover the following methods for both ETH and BSC clients:

- `get_last_block_number`: Tests the retrieval of the latest block number.

- `get_balance`: Tests the retrieval of account balances with different wallet addresses.

- `get_transaction`: Tests the retrieval of transaction details using transaction hashes.

- `get_contract_balance`: Tests the retrieval of token balances for different wallet addresses and contract addresses.

- `get_transactions_count`: Tests the retrieval of transaction counts for different wallet addresses.

- `get_gas_price`: Tests the retrieval of the current gas price.

- `send`: Tests the sending of transactions with various parameters, such as private keys, recipient addresses, amounts, gas prices, and gas limits.

- `get_contract_decimals`: Tests the retrieval of the number of decimals for a given contract address.

- `send_token`: Tests the sending of token transactions with different parameters, including private keys, recipient addresses, contract addresses, amounts, gas prices, and gas limits.

Test Parameters
---------------

The tests utilize parameterized test cases to cover a wide range of scenarios. The test parameters include:

- Valid and invalid wallet addresses
- Valid and invalid transaction hashes
- Valid and invalid contract addresses
- Different amounts for transactions and token transfers
- Different gas prices and gas limits
- Expected exceptions for error scenarios

The test cases ensure that the clients handle both successful and error scenarios gracefully and raise the appropriate exceptions when necessary.

VCR (Video Cassette Recorder)
-----------------------------

The AioTx test suites use the VCR library to record and replay network interactions during testing. VCR allows the tests to run independently of the actual Ethereum and Binance Smart Chain networks, providing a consistent and controlled testing environment.

When a test is run for the first time with VCR, it records the network interactions and stores them in YAML files (cassettes). Subsequent test runs use the recorded interactions instead of making actual network requests, ensuring fast and deterministic test execution.

The VCR cassettes are stored in separate directories for each client (`eth` and `bsc`) and are named according to the tested method and scenario.

It's important to note that due to the use of VCR, some tests may raise exceptions related to transaction replacement (`ReplacementTransactionUnderpriced`) or nonce-related errors (`NonceTooLowError`). This is because the recorded network interactions may not always match the expected state of the blockchain at the time of testing. These limitations are documented in the test cases.

Testing Different Networks
--------------------------

The AioTx test suites cover both the Ethereum (ETH) and Binance Smart Chain (BSC) networks. The tests are organized into separate directories (`eth` and `bsc`) to maintain clarity and separation between the network-specific test cases.

The test cases for each network use distinct contract addresses, wallet addresses, and transaction hashes to ensure the correctness of the client methods in the context of each network.

Conclusion
----------

The AioTx test suites provide comprehensive coverage of the Ethereum (ETH) and Binance Smart Chain (BSC) clients. By utilizing parameterized test cases, VCR for network interaction recording, and testing across different networks, the test suites ensure the reliability and correctness of the client methods. The tests serve as a safety net for detecting regressions and verifying the expected behavior of the AioTx clients.