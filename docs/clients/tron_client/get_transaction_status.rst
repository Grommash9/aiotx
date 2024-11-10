get_transaction_status
======================

.. code-block:: python

    async get_transaction_status(tx_id: str) -> dict

Get the status and details of a transaction by its ID.

https://developers.tron.network/reference/wallet-gettransactionbyid

Parameters:
 - **tx_id** (str): The transaction ID.

Returns:

.. code-block:: python

    {  
    "ret":[  
        {  
            "contractRet":"SUCCESS"
        }
    ],
    "signature":[  
        "ffbf691a89d95f6ad8175611c7d334c8159b95ff9c1e83872e7670103b185e85faf0a394b23d99581385d38038ab5c4684759c864a5621009f6e95da0a5feab501"
    ],
    "txID":"d0807adb3c5412aa150787b944c96ee898c997debdc27e2f6a643c771edb5933",
    "raw_data":{  
        "contract":[  
            {  
                "parameter":{  
                "value":{  
                    "amount":16,
                    "asset_name":"54726f6e696373",
                    "owner_address":"414a5fe0179f2dd9c900194e63d661863cd0ade7b0",
                    "to_address":"41718de6b323652d1257437ace160c4f4198aae4e1"
                },
                "type_url":"type.googleapis.com/protocol.TransferAssetContract"
                },
                "type":"TransferAssetContract"
            }
        ],
        "ref_block_bytes":"6bdd",
        "ref_block_hash":"1616edaf3a57fe19",
        "expiration":1546455678000,
        "timestamp":1546455620175
    }
    }

Raises:
 - **TransactionNotFound**: If the transaction is not found.
 - **InvalidArgumentError**: invalid hash value
 - **RpcConnectionError**: RpcConnectionError

Example usage:

.. code-block:: python

    tron_client = AioTxTRONClient("NODE_URL")
    
    # Get transaction status
    status = await tron_client.get_transaction_status(
        "1eb454389c148f9b0e3fb458fffcb37569b6498d87b4945fbdef4d266c64089b"
    )
    print("Transaction status:", status)

Example output trx transaction 68bc7cf2fa0a356be43f893ff7466d26edbd86bf5874c1f8398b4a0662ee2e71:

.. code-block:: python

    {
        "ret": [
            {
                "contractRet": "SUCCESS"
            }
        ]
    }

Part of example output from trc20 OUT_OF_ENERGY e63a324a43aebfe41273db4f7fdfe325b2257b4f5711595a5fc0f8a75cf1b481:

.. code-block:: python

    {
        "ret": [
            {
            "contractRet": "OUT_OF_ENERGY"
            }
        ]
    }

Part of example output from trc20 SUCCESS:

.. code-block:: python

    {
        "ret": [
            {
            "contractRet": "SUCCESS"
            }
        ]
    }

The `get_transaction_status` method provides a simple way to check if a transaction has been confirmed and was successful. This is particularly useful for:
- Monitoring transaction confirmations
- Verifying successful contract interactions
- Checking energy consumption
- Error handling for failed transactions

**Note:** The transaction ID should be a valid TRON transaction hash. For TRC20 token transfers or contract interactions, the `contract_result` field will contain relevant execution results.

Possible status codes
https://github.com/tronprotocol/java-tron/blob/develop/Tron%20protobuf%20protocol%20document.md

DEFAULT = 0;

SUCCESS = 1;

REVERT = 2;

BAD_JUMP_DESTINATION = 3;

OUT_OF_MEMORY = 4;

PRECOMPILED_CONTRACT = 5;

STACK_TOO_SMALL = 6;

STACK_TOO_LARGE = 7;

ILLEGAL_OPERATION = 8;

STACK_OVERFLOW = 9;

OUT_OF_ENERGY = 10;

OUT_OF_TIME = 11;

JVM_STACK_OVER_FLOW = 12;

UNKNOWN = 13;

TRANSFER_FAILED = 14;
