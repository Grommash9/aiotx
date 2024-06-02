from aiotx.clients import AioTxTRONClient
import asyncio

tron_client = AioTxTRONClient(node_url="https://go.getblock.io/1588be2555b3472e89b2cd58899415cb/jsonrpc")



async def main():

    balance = await tron_client.get_balance("TVXFMCXZsEZQbj1VszDw91G7uvNncBxnMw")
    print(balance, "balance")

    balance = await tron_client.get_contract_balance("TWjsZKUonHdiG4r4YuF9RAXXDo5ryicPuN", "TXLAQ63Xg1NAzckPwKHvzw7CSEmLMEqcdj")
    print(balance, "balance")

    tx_data = await tron_client.get_transaction("0x2ee04f0cc089e1f1d2499c1f7ee3114a69a61dda478c39ea2d1becdd97d387fa")
    print("tx_data", tx_data)

    get_chain_id = await tron_client.get_chain_id()
    print("get_chain_id", get_chain_id)

    decimals = await tron_client.get_contract_decimals("TXLAQ63Xg1NAzckPwKHvzw7CSEmLMEqcdj")
    print("decimals", decimals)


if __name__ == "__main__":
    asyncio.run(main())