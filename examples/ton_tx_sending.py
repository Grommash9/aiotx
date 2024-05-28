from aiotx.clients import AioTxTONClient
import asyncio

ton_client = AioTxTONClient("https://testnet.toncenter.com/api/v2/jsonRPC", workchain=0)
# We are adding workchain here because testnet.toncenter working bad and identify itself as -1 but it should be 0
# If you are using any other provider it should work fine without workchain param

amount = ton_client.to_nano(0.0001)
mnemonic_str = "post web slim candy example glimpse other reduce layer way ordinary hidden dwarf marble fancy gym client soul speed enforce drift huge upset oblige"

balance = asyncio.run(ton_client.get_balance("UQDU1hdX6SeHmrvzvyjIrLEWUAdJUJar2sw8haIuT_5n-FLh"))

tx_id = asyncio.run(ton_client.send(mnemonic_str, "0QAEhA1CupMp7uMOUfHHoh7sqAMNu1xQOydf8fQf-ATpkbpT", amount))
print(tx_id)
