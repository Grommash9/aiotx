# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [6.0.0]
- Move timeout between blocks for TON outside of shards logic
    - Before
        - We had a delay between all the shards of master block
    - Now
        - We well have a delay only when our latest block is bigger to network latests (we are up to date)
    It should speed up TON block monitoring but you know will get 429 limits on free tiers for sure
    Maybe later more variables will be added to cover TON network monitoring

## [5.1.0]
- revert all the changes from 5.0.0

## [5.0.0]
- send exit signal on any error in monitoring

## [4.12.0]
- Add tron get transaction info method (working on quicknode/tatum)

## [4.11.0]
- Add tron get transaction status method (working on quicknode/tatum)

## [4.10.0]
- add new utxo transaction for new UTXO transactions

## [4.9.0]
- Add current and latest block for EMV based clients

## [4.8.0]
- Monitoring - raising errors on any fails inside of it (was silently failing before)

## [4.7.1]
- Remove rewriting workchain id param for TON if we already have it


## [4.7.0]
- Monitoring - added handler for getting all block transactions `on_block_transactions`

## [4.6.1]
- TRON fix decoding trc20 transactions with 41 address prefix

## [4.6.0]
- TON add transfer jettons method

## [4.5.0]
- TON add get jetton address and get jetton balance methods

## [4.4.0]
- raise an error on failed tron transaction send

## [4.3.0]
- fix to sun converting with decimals

## [4.2.0]
- fix TRON address converting for tokens sending

## [4.1.0]
- UTXO client typehint for UTXO added :D
- added speed_up_transaction_by_self_child_payment function

## [4.0.0]
- imports logic change for having extras
- UTXO client get transaction fee and get raw transaction methods added

## [3.0.6]
- evm client decoding error ignore added

## [3.0.5]
- fix sleep for TON monitoring timeout between shards 

## [3.0.4]
- add wait for shard polling TON client

## [3.0.3]
- adding info logger for all rpc/api calls

## [3.0.2]
- utxo client to satoshi fix math for to_satoshi function

## [3.0.1]
- UTXO client satoshi data storage logic fix

## [3.0.0]
- query_id logic fixed for TON bulk send now you can send bulk transactions one by one without issues

## [2.11.2]
- Remove silent error printing from block monitoring, now it will raise any errors

## [2.10.2]
- TRON memo by default logic fixed

## [2.10.1]
- timeout_between_blocks optional param added to block monitoring
- optional headers param added to all client 
- add jsonRPC into TON url by default and Deprication warning added

## [2.9.1]
- remove not tested python versions from pypi list 

## [2.9.0]
- TON client bulk TON send added

## [2.8.0]
- TRON client send TRX and send TRC20 functions added and covered by tests, docs updated

## [2.7.1]
- TON client memo added to send operation

## [2.7.0]
- TRON client monitoring/wallet generation/get balance added
- Node connection error is now RpcConnectionError
- BTC init with failed get last block will do warning but not crash all code

## [2.6.0]
- to_wei from_wei added hex numbers logic support / docs updated

## [2.5.0]
- RpcConnectionError error added to be raised if there is any issues with connection to node

## [2.4.0]
- EVM client `to_wei` and `from_wei` default value `ether` added

## [2.3.0]
- Remove tonsdk library dep because we don't want to use `bitarray` from that to avoid need of C++ for windows

## [2.2.0]
- TON monitoring/generate wallet/send/get transactions added

## [2.1.0]
- Polygon client added and covered by tests
- EVM client send token function change to convert contract address to_checksum_address by default

## [2.0.0]
- BREAKING change - EVM chain ID parameter removed from client definition

## [1.3.0]
- Pulling block only if they are in network to stop printing a lot of errors

## [1.2.5]
- Pin the version of main packages and code changes for new eth_account 

## [1.2.4]
- Add setuptoools to support python 3.12

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
