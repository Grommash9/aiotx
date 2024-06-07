from aiotx.clients import AioTxTRONClient
import asyncio

tron_client = AioTxTRONClient(node_url="https://api.shasta.trongrid.io")


async def main():

    # wallet = tron_client.generate_tron_address()
    # print(wallet)


    # balance = await tron_client.get_balance("TEZQQ5BXq3nFKUFJknoV15CW24twzH81La")
    # print("balance", balance)

    # account_data = await tron_client.get_account("TEZQQ5BXq3nFKUFJknoV15CW24twzH81La")
    # print("account_data", account_data)

    # tx_data = await tron_client.send("",
    #                                  "TYge3Gid6vVaQvnPVRJ6SVwzC64cw2eBkN",
    #                                  100000,
    #                                  memo="Test for Melanty")
    # print("tx_data", tx_data)

    # tx_info = await tron_client.get_transaction("11aa7f0568271a77039cd7cb318dc446e54461332aea659a9e0a8928f6480333")
    # print("tx_info", tx_info)
    

    # tx_data = await tron_client._create_trc20_transfer_transaction(
    #     "TEZQQ5BXq3nFKUFJknoV15CW24twzH81La", "TYge3Gid6vVaQvnPVRJ6SVwzC64cw2eBkN",
    #     11111, "TG3XXyExBkPp9nzdajDZsozEu4BkaSJozs", memo="privetpop"
    # )
    # print("tx_data", tx_data)

    tx_data = await tron_client.send_token("",
                                           "TYge3Gid6vVaQvnPVRJ6SVwzC64cw2eBkN",
                                           "TG3XXyExBkPp9nzdajDZsozEu4BkaSJozs",
                                           1999,
                                           memo="privetpop")


    print("tx_data", tx_data)


    # solii = await tron_client.get_latest_solidity_block()
    # print("solii", solii)

    # tx_data = await tron_client.create_transaction("TEZQQ5BXq3nFKUFJknoV15CW24twzH81La",
    #                                                "TYge3Gid6vVaQvnPVRJ6SVwzC64cw2eBkN",
    #                                                1000)
    # ""

if __name__ == "__main__":
    asyncio.run(main())