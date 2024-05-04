EVM client
==========

Introduction
------------

The Ethereum Virtual Machine (EVM) Client is a parent client for networks based on the EVM, including Ethereum (**ETH**), Binance Smart Chain (**BSC**), Polygon (**MATIC**), Avalanche (**AVAX**), Fantom (**FTM**), Cronos (**CRO**), Harmony (**ONE**), and more.

All of these cryptocurrencies use similar logic in many places, so they will be merged into the same parent client.

Currently, AioTxBSCClient and AioTxETHClient are tested and ready to be used. Please keep in mind that when reading this documentation, the methods can be used for any EVM-based blockchain.

QuickStart (**Logic is the same for all EVM clients; just import AioTxBSCClient or AioTxETHClient**)

--------------------

To create an instance of AioTxETHClient, you need to provide the ETH node URL and the chain ID. Here's an example:

.. code-block:: python

   from aiotx.clients import AioTxETHClient
   import asyncio


   async def main():
      eth_client = AioTxETHClient("NODE_URL", "ETH_CHAIN_ID")

      last_block = await eth_client.get_last_block_number()
      print("last_block", last_block)

      tx_data = await eth_client.get_transaction("tx_id")
      print("tx_data", tx_data)

      contract_decimals = await eth_client.get_contract_decimals(
         "contract_address"
         )
      print("contract_decimals", contract_decimals)

      # Getting ETH balance
      balance = await eth_client.get_balance("address")
      print("balance", balance)

      # Getting USDT balance
      contract_balance = await eth_client.get_contract_balance(
         "address", "contract_address"
         )
      print("contract_balance", contract_balance)

      # Sending 0.5 ETH
      amount_in_wei = eth_client.to_wei(0.5)
      tx_id = await eth_client.send(
         "private_key", "to_address", amount_in_wei
         )

      # Sending 10 USDT (ERC20)
      # (Contract has 6 decimals; please check decimals!)
      amount_in_wei = eth_client.to_wei(10, "mwei")
      tx_id = await eth_client.send_token(
         "private_key", "to_address", 
         "usdt_contract_address", amount_in_wei)

   asyncio.run(main())

Methods
-------

.. toctree::
   :maxdepth: 1

   generate_address
   get_address_from_private_key
   get_balance
   get_last_block
   get_block_by_number
   get_transaction_count
   get_transaction
   from_wei
   to_wei 
   get_gas_price
   send
   get_contract_balance
   get_contract_decimals
   send_token
   