from aiotx.clients import AioTxTRONClient
import asyncio

tron_client = AioTxTRONClient(node_url="https://api.shasta.trongrid.io")


async def main():
    balance = await tron_client.get_balance("TEZQQ5BXq3nFKUFJknoV15CW24twzH81La")
    print("balance", balance)

    account_data = await tron_client.get_account("TEZQQ5BXq3nFKUFJknoV15CW24twzH81La")
    print("account_data", account_data)

    tx_data = await tron_client.send("",
                                     "TYge3Gid6vVaQvnPVRJ6SVwzC64cw2eBkN",
                                     1000)
    print("tx_data", tx_data
    )

    # solii = await tron_client.get_latest_solidity_block()
    # print("solii", solii)

    # tx_data = await tron_client.create_transaction("TEZQQ5BXq3nFKUFJknoV15CW24twzH81La",
    #                                                "TYge3Gid6vVaQvnPVRJ6SVwzC64cw2eBkN",
    #                                                1000)
    # ""

if __name__ == "__main__":
    asyncio.run(main())