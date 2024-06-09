import asyncio

from aiotx.clients import AioTxTRONClient

tron_client = AioTxTRONClient(node_url="https://api.shasta.trongrid.io")


async def main():
    wallet = tron_client.generate_address()
    print(wallet)

    balance = await tron_client.get_balance("TEZQQ5BXq3nFKUFJknoV15CW24twzH81La")
    print("balance", balance)

    tx_data = await tron_client.send(
        "private_key",
        "TYge3Gid6vVaQvnPVRJ6SVwzC64cw2eBkN",
        100000,
        memo="Test for Melanty",
    )
    print("tx_data", tx_data)

    tx_data = await tron_client.send_token(
        "private_key",
        "TYge3Gid6vVaQvnPVRJ6SVwzC64cw2eBkN",
        "TG3XXyExBkPp9nzdajDZsozEu4BkaSJozs",
        1999,
        memo="privetpop",
    )
    print("tx_data", tx_data)


if __name__ == "__main__":
    asyncio.run(main())
