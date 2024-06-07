from aiotx.clients import AioTxTONClient
import asyncio


# ton_client = AioTxTONClient("https://testnet.toncenter.com/api/v2/jsonRPC", workchain=0)
# # We are adding workchain here because testnet.toncenter working bad and identify itself as -1 but it should be 0
# # If you are using any other provider it should work fine without workchain param


# # wallet = asyncio.run(ton_client.generate_address())
# # print("wallet", wallet)

# amount = ton_client.to_nano(0.0001)
# mnemonic_str = "truck salt rib coffee fold tree album often rice nominee green minor lemon ritual gossip divorce monkey garment symbol super lonely liar pond coin"

# # balance = asyncio.run(ton_client.get_balance("UQDU1hdX6SeHmrvzvyjIrLEWUAdJUJar2sw8haIuT_5n-FLh"))

# tx_id = asyncio.run(
#     ton_client.send(
#         mnemonic_str,
#         "0QAEhA1CupMp7uMOUfHHoh7sqAMNu1xQOydf8fQf-ATpkbpT",
#         amount,
#         memo="for Melanty with love",
#     )
# )
# print(tx_id)

### Multi send:

from aiotx.utils.tonsdk.contract.wallet import Wallets, WalletVersionEnum

ton_client = AioTxTONClient("https://testnet.toncenter.com/api/v2/jsonRPC", workchain=0, wallet_version=WalletVersionEnum.hv2)


wallet = asyncio.run(ton_client.generate_address())
print("wallet", wallet)

wallet_result = (
    'desert buddy wheat loan large snow vehicle possible orbit rich program flame recycle rail cancel derive force spoon refuse swarm era shoe repair front',
    'UQBpmxXlO28nZgIWGCcEnegs1qzPzULitm4VuyXYXhV2Z2pv',
    '0:699b15e53b6f276602161827049de82cd6accfcd42e2b66e15bb25d85e157667')


tx_id = asyncio.run(ton_client.send_bulk("desert buddy wheat loan large snow vehicle possible orbit rich program flame recycle rail cancel derive force spoon refuse swarm era shoe repair front"))

print("tx_id", tx_id)