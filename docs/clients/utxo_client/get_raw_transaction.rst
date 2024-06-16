get_raw_transaction
===================

.. code-block:: python
    
    get_raw_transaction(
        tx_id: str, 
        verbosity: int = 2
        ) -> dict



The ``get_raw_transaction`` function retrieves raw transaction data from the node. 

It takes a transaction ID (TXID) and an optional verbosity level as input parameters and returns a dictionary containing the raw transaction data.


Parameters:

   - **tx_id** (str): The transaction ID (TXID) of the transaction to retrieve.
   - **verbosity** (int, optional) : The verbosity level for the transaction data. Defaults to 2. (return type can be different)

Returns:

   - **dict**: A dictionary containing the raw transaction data.

Raises:

   - **RpcConnectionError**:  If there is an error connecting to the Bitcoin node or making the RPC call.


Example:

.. code-block:: python

    tx_data = await btc_client.get_raw_transaction(
        '35158b7a8b6057bc67f6d904c64b5986adea8260f0bc96cbd755b530878e3cc2'
        )

    print(tx_data)
    # Output: 
    {
    "txid": "c966837e3a29863341e3e85702152f479e97cd80e63684ddb2061c7c5cf92851",
    "hash": "d83b394898c81d95918da2f7300822534efdc6e926a9e44f4ea563b36e4df040",
    "version": 2,
    "size": 283,
    "vsize": 202,
    "weight": 805,
    "locktime": 0,
    "vin": [
        {
            "ismweb": false,
            "txid": "008d89fae54adb20125a96673336a9ce3886358984b9c701d41b0d823f237cc3",
            "vout": 0,
            "scriptSig": {
                "asm": "",
                "hex": ""
            },
            "txinwitness": [
                "304402207b562c1a04de15b4eca848b9dc3d557d56871cea0178670036a3be5921232ee4022028bb5eddb47f7e16c5e73e997e0ed665baec5875fd014162cc821431d4d19d9401",
                "03369f8a894c7793bb78bfe8a8938031a0e204dac3451f527eeac3f271d2acca0e"
            ],
            "sequence": 4294967295
        }
    ],
    "vout": [
        {
            "ismweb": false,
            "value": 3.01859589,
            "n": 0,
            "scriptPubKey": {
                "asm": "0 554e946799fe176568ec4fc2a7078f5ebc14f6c8",
                "hex": "0014554e946799fe176568ec4fc2a7078f5ebc14f6c8",
                "reqSigs": 1,
                "type": "witness_v0_keyhash",
                "addresses": [
                    "tltc1q248fgeuelctk268vflp2wpu0t67pfakgw6s3mu"
                ]
            }
        },
        {
            "ismweb": false,
            "value": 0,
            "n": 1,
            "scriptPubKey": {
                "asm": "OP_RETURN ab3038204bd9438ebd230affc2145a11483f8dcf05c7e5c5597bbdc3f6f699bc3adcfc073cd4fd3d57fc1121ad0888418c665dcbcd732a3952b2d33a46e97336fcfe192ec6b85453c8c7af6aaa9310f7",
                "hex": "6a4c50ab3038204bd9438ebd230affc2145a11483f8dcf05c7e5c5597bbdc3f6f699bc3adcfc073cd4fd3d57fc1121ad0888418c665dcbcd732a3952b2d33a46e97336fcfe192ec6b85453c8c7af6aaa9310f7",
                "type": "nulldata"
            }
        }
    ],
    "hex": "02000000000101c37c233f820d1bd401c7b98489358638cea9363367965a1220db4ae5fa898d000000000000ffffffff020503fe1100000000160014554e946799fe176568ec4fc2a7078f5ebc14f6c80000000000000000536a4c50ab3038204bd9438ebd230affc2145a11483f8dcf05c7e5c5597bbdc3f6f699bc3adcfc073cd4fd3d57fc1121ad0888418c665dcbcd732a3952b2d33a46e97336fcfe192ec6b85453c8c7af6aaa9310f70247304402207b562c1a04de15b4eca848b9dc3d557d56871cea0178670036a3be5921232ee4022028bb5eddb47f7e16c5e73e997e0ed665baec5875fd014162cc821431d4d19d94012103369f8a894c7793bb78bfe8a8938031a0e204dac3451f527eeac3f271d2acca0e00000000",
    "blockhash": "3f4a8f7e531ee281ae61811554070f41f8cfebd0057508cc5959c94ad65c5fd9",
    "confirmations": 396,
    "time": 1718510178,
    "blocktime": 1718510178
    }

