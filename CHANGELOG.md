# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [1.2.3]
- EVM client fix, using pkg_resources to get abi files

## [1.2.2]
- EVM client fix, jsons added for build now second try (what a shame D:)

## [1.2.1]
- EVM client fix, jsons added for build now

## [1.2.0]
- UTXO client - adding UTXOs after send, so we will able to send few transactions in same block
    without waiting for new one to get our UTXOs

## [1.1.0]
- UTXO client hotfix - we should have keys for all used inputs and not just for all inputs

## [1.0.0]
- LTC/BTC logic and tests added

## [0.6.0]
- UTXO client block monitoring logic added and tested for LTC and BTC (both covered by tests)

## [0.5.1]
- EVM client docs added

## [0.5.0]
- AioTxETHClient covered by tests and ready to be used
- nonce is now optional param to give users enter in manually for sending transactions faster
- get_contract_decimals function added for EVMClient, now you can get decimals for contracts

## [0.4.0]
- Added tests for send and send_token function, they was renamed and changed, getting pending for nonce now

## [0.3.0]
- Function for getting current gas price is added and to_wai/from_wai functions are attached to EVM client now

## [0.2.0]
- block/transactions monitoring added, examples of usage added, tx input decoding added

## [0.1.0]
- EVM client base logic added (get_balance, send tokens)
- tests added

## [0.0.10]
- EVM networks wallet generation logic added

## [0.0.5]
- empty (auto pypi testing)

## [0.0.3]

- project skeleton has been added

## [0.0.2]

- project metadata added

## [0.0.1]

- repo created, initial codebase added
