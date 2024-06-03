TRON client
===========


QuickStart 
----------

To create an instance of AioTxTRONClient, you need to provide the node URL and. Here's an example:

.. code-block:: python

   from aiotx.clients import AioTxTRONClient
   import asyncio

   tron_client = AioTxTRONClient("NodeUrl")


   async def main():
      last_block = await tron_client.get_last_block_number()
      print("last_block", last_block)
      Output: last_block 47393539

      tx_data = await tron_client.get_transaction(
         "83033077a7a5ea6e07fa1e36069886daf3abe8bae4e12168391db9c0b28002a7"
         )
      print("tx_data", tx_data)
      Output: tx_data {'blockHash': '0x0000000002d323756e1ec99201904db3f1a9225219604f09f0d9bfcec2739a95', 
      'blockNumber': '0x2d32375', 'from': '0x4833b7e7d199642e76087829128c734b9555dd3d', 'gas': '0x3476', 
      'gasPrice': '0x1a4', 'hash': '0x83033077a7a5ea6e07fa1e36069886daf3abe8bae4e12168391db9c0b28002a7', 
      'input': '0xa9059cbb0000000000000000000000001697bb7f2eafc85571423577c956fb70003d06630000000000000000000000000000000000000000000000000000000011e1a300', 
      'nonce': '0x0000000000000000', 'r': '0x2d386c10d4f0dd79ee4b1dae647ae618acbe9dad48398e8f6781719b71b60d83', 
      's': '0x7de329f8a2a19de8b7dcfb969640c3b75a8d29110573d431499f2de9973472d7', 
      'to': '0xea51342dabbb928ae1e576bd39eff8aaf070a8c6', 'transactionIndex': '0x0', 
      'type': '0x0', 'v': '0x1b', 'value': '0x0', 
      'aiotx_decoded_input': {'function_name': 'transfer', 
      'parameters': {'_to': '0x1697bb7f2eafc85571423577c956fb70003d0663', 
      '_value': 300000000}}}

      contract_decimals = await tron_client.get_contract_decimals(
         "TXLAQ63Xg1NAzckPwKHvzw7CSEmLMEqcdj"
         )
      print("contract_decimals", contract_decimals)
      Output: contract_decimals 6

      # Getting TRX balance
      balance = await tron_client.get_balance(
         "TEZQQ5BXq3nFKUFJknoV15CW24twzH81La"
         )
      print("balance", balance)
      Output: balance 4001000000

      # Getting USDT balance
      contract_balance = await tron_client.get_contract_balance(
         "TEZQQ5BXq3nFKUFJknoV15CW24twzH81La", 
         "TXLAQ63Xg1NAzckPwKHvzw7CSEmLMEqcdj"
         )
      print("contract_balance", contract_balance)
      Output: contract_balance 50000000000

   asyncio.run(main())

Methods
-------

.. toctree::
   :maxdepth: 1

   generate_address
   get_balance
   get_contract_balance
   get_contract_decimals
   get_last_block
   get_transaction

   