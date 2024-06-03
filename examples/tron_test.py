from aiotx.clients import AioTxTRONClient
import asyncio

tron_client = AioTxTRONClient("https://go.getblock.io/d5d80fb886f2401a98a7f4fe57d88839")



async def main():
    wallet = tron_client.generate_address()
    print("wallet", wallet)


    # tx_data = await tron_client.get_transaction("bee7c8234683d0835878b7ee04094af486593d5a1042f060a17e35e5fe9a5b22")
    # print("tx_data", tx_data)

    # base58_address = tron_client.hex_address_to_base58("0xd3682962027e721c5247a9faf7865fe4a71d5438")
    # print(base58_address)


if __name__ == "__main__":
    asyncio.run(main())