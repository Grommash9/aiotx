get_transaction_info
====================

.. code-block:: python

   async get_transaction_info(tx_id: str) -> dict

Query transaction information including fee, block height, and execution results by transaction ID.

Parameters:

   - **tx_id** (str): Transaction hash/ID to query
   
Returns:
    - Dictionary containing transaction information
   
   The returned dictionary contains the following fields:

   - ``id`` (str): Transaction ID
   - ``fee`` (int): Total TRX burned (including bandwidth/energy costs, memo fee, etc.)
   - ``blockNumber`` (int): Block number containing the transaction
   - ``blockTimeStamp`` (int): Block timestamp in milliseconds
   - ``contractResult`` (List[str]): Transaction execution results
   - ``contract_address`` (str, optional): Contract address if applicable
   
   **Receipt Information**
   
   - ``receipt`` (dict): Transaction receipt containing:
     
     - ``energy_usage`` (int): Energy consumed by caller's account
     - ``energy_fee`` (int): TRX burned for energy
     - ``origin_energy_usage`` (int): Energy consumed by contract deployer
     - ``energy_usage_total`` (int): Total energy consumed
     - ``net_usage`` (int): Bandwidth consumed
     - ``net_fee`` (int): TRX burned for bandwidth
     - ``result`` (str): Execution result
     - ``energy_penalty_total`` (int): Extra energy cost for popular contracts

   **Event Logs**
   
   - ``log`` (List[dict], optional): Smart contract event logs containing:
     
     - ``address`` (str): Contract address (hex format)
     - ``topics`` (List[str]): Event topics and indexed parameters
     - ``data`` (str): Non-indexed event parameters

   **Additional Fields**
   
   - ``result`` (str, optional): "FAILED" if transaction failed
   - ``resMessage`` (str, optional): Failure details in hex format if failed
   - ``withdraw_amount`` (int, optional): Withdrawn vote rewards in sun
   - ``unfreeze_amount`` (int, optional): Unstaked TRX amount in sun (Stake1.0)
   - ``withdraw_expire_amount`` (int, optional): Unfrozen TRX withdrawn in sun (Stake2.0)
   - ``cancel_unfreezeV2_amount`` (dict, optional): Re-staked TRX amounts by resource type

   **Example**::

        # Query transaction information
        tx_info = await client.get_transaction_info(
            "7c2d4206c03a883dd9066d620335dc1be272a8dc733cfa3f6d10308faa37facc"
        )
        
        # Access transaction details
        block_number = tx_info["blockNumber"]
        energy_used = tx_info["receipt"]["energy_usage_total"]

Raises:

    - **TransactionNotFound**: If the transaction cannot be found  
    - **RpcConnectionError**: If there is an error connecting to the RPC node


Example output trx trc20 failed transaction b69c51db8f9d974e6a38c76852c8ce1adcb682dbacb25ad8ad4f6876121fe9dc:

.. code-block:: python

    {
    "id": "b69c51db8f9d974e6a38c76852c8ce1adcb682dbacb25ad8ad4f6876121fe9dc",
    "fee": 345000,
    "blockNumber": 66861993,
    "blockTimeStamp": 1731235554000,
    "contractResult": [
        "0000000000000000000000000000000000000000000000000000000000000000"
    ],
    "contract_address": "41a614f803b6fd780986a42c78ec9c7f77e6ded13c",
    "receipt": {
        "energy_usage": 64285,
        "energy_usage_total": 64285,
        "net_fee": 345000,
        "result": "SUCCESS",
        "energy_penalty_total": 49635
    },
    "log": [
        {
            "address": "a614f803b6fd780986a42c78ec9c7f77e6ded13c",
            "topics": [
                "ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
                "00000000000000000000000060e6e92e57d61a9d68b5d95275cc9667d9e6c7c9",
                "000000000000000000000000cdae4e9a6287333a3f7df432b050af7b17e79e63"
            ],
            "data": "00000000000000000000000000000000000000000000000000000000003567e0"
        }
    ]
    }


Example output trx trc20 failed transaction e63a324a43aebfe41273db4f7fdfe325b2257b4f5711595a5fc0f8a75cf1b481:

.. code-block:: python

    {
    "id": "e63a324a43aebfe41273db4f7fdfe325b2257b4f5711595a5fc0f8a75cf1b481",
    "fee": 16500120,
    "blockNumber": 66860010,
    "blockTimeStamp": 1731229605000,
    "contractResult": [
        ""
    ],
    "contract_address": "41a614f803b6fd780986a42c78ec9c7f77e6ded13c",
    "receipt": {
        "energy_fee": 16500120,
        "energy_usage_total": 78572,
        "net_usage": 345,
        "result": "OUT_OF_ENERGY",
        "energy_penalty_total": 25905
    },
    "result": "FAILED",
    "resMessage": "4e6f7420656e6f75676820656e6572677920666f7220275353544f524527206f7065726174696f6e20657865637574696e673a20637572496e766f6b65456e657267794c696d69745b37383537325d2c206375724f70456e657267795b32303030305d2c2070656e616c7479456e657267795b36383030305d2c2075736564456e657267795b33333536375d"
    }


Example output trx transaction 2389719608ed69f7ec3e72c1abb92acaa43b7175f3062f4ebc6e2e02cc82d0d2:

.. code-block:: python

    {
    "id": "2389719608ed69f7ec3e72c1abb92acaa43b7175f3062f4ebc6e2e02cc82d0d2",
    "blockNumber": 66862205,
    "blockTimeStamp": 1731236190000,
    "contractResult": [
        ""
    ],
    "receipt": {
        "net_usage": 265
    }
    }


    