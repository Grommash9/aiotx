estimate_smart_fee
==================

.. code-block:: python

   async def estimate_smart_fee(
       conf_target: int = 6,
       estimate_mode: FeeEstimate = FeeEstimate.CONSERVATIVE
   ) -> int:

Estimates the smart fee for a transaction based on the specified confirmation target and estimate mode.

Parameters:
   - **conf_target** (int, optional): The desired confirmation target in blocks. Default is 6 blocks.
   - **estimate_mode** (FeeEstimate, optional): The estimate mode to use. Default is `FeeEstimate.CONSERVATIVE`.

Returns:
   - int: The estimated smart fee in satoshis per byte.

The `estimate_smart_fee` method estimates the appropriate fee per byte to use for a transaction based on the specified confirmation target and estimate mode. It uses the `estimatesmartfee` RPC method of the Bitcoin Core node to retrieve the estimated fee rate.

The method takes two optional parameters:

1. `conf_target`: The desired confirmation target in blocks. It represents the number of blocks within which the transaction should be confirmed. The default value is 6 blocks.

2. `estimate_mode`: The estimate mode to use for fee estimation. It is specified using the `FeeEstimate` enum, which has the following values:
   - `FeeEstimate.UNSET`: The default estimate mode used by the node.
   - `FeeEstimate.ECONOMICAL`: Estimates the fee rate for a transaction to be confirmed within the specified `conf_target` with a lower fee, potentially taking longer to confirm.
   - `FeeEstimate.CONSERVATIVE` (default): Estimates the fee rate for a transaction to be confirmed within the specified `conf_target` with a higher fee, aiming for faster confirmation.

The method constructs an RPC payload with the `estimatesmartfee` method and the provided `conf_target` and `estimate_mode` as parameters. It then sends the RPC request to the Bitcoin node using the `_make_rpc_call` method.

The response from the node includes the estimated fee rate in BTC per kilobyte. The method extracts the `feerate` value from the response and converts it from BTC to satoshis using the `to_satoshi` helper method. Finally, it returns the estimated smart fee in satoshis per byte.

Example usage:

.. code-block:: python

   # Estimate the smart fee for a confirmation target of 6 blocks
   smart_fee = await btc_client.estimate_smart_fee(
    conf_target=6
    )
   print(f"Estimated smart fee: {smart_fee} satoshis/byte")

   # Estimate the smart fee for a confirmation 
   # target of 3 blocks using the economical mode
   smart_fee_economical = await btc_client.estimate_smart_fee(
    conf_target=3, 
    estimate_mode=FeeEstimate.ECONOMICAL
    )
   print(f"Estimated smart fee: {smart_fee_economical} satoshis/byte")

In the first example, the `estimate_smart_fee` method is called with the default confirmation target of 6 blocks. The estimated smart fee is printed in satoshis per byte.

In the second example, the `estimate_smart_fee` method is called with a confirmation target of 3 blocks and the `FeeEstimate.ECONOMICAL` estimate mode. The estimated smart fee using the economical mode is printed in satoshis per byte.

Note: The estimated smart fee is based on the current network conditions and can vary over time. It is important to consider the desired confirmation target and estimate mode when estimating the fee to balance between transaction confirmation speed and fee cost.