import asyncio

from aiotx.clients import AioTxBTCClient

BTC_TEST_NODE_URL = "https://ultra-special-dust.btc-testnet.quiknode.pro/331c45aef598f74795cef49fd7e5be98d37d7f06/"
btc_client = AioTxBTCClient(BTC_TEST_NODE_URL, testnet=True)


private_key = "f92e4728b012829158028e4343d602b8187aa50cd2c03651c6fc95168af2e606"
address = "tb1qswslzcdulvlk62gdrg8wa0sw36f938h2pyfreh"
to_address = "tb1q3t09ltyprf9djw244yt7xa2wumck8qav489km5"


async def main():

    await btc_client.import_address(address)

    # await btc_client.monitor._add_new_utxo(address, "cf917450acb35ffaf313b25efe5f02cb927f22e7aed12300912bd98421c0c616",
    #                                        btc_client.to_satoshi(283.68202744), 1)

    # balance = await btc_client.get_balance(
    #     "tb1qswslzcdulvlk62gdrg8wa0sw36f938h2pyfreh"
    # )
    # print("balance is:", balance)
    # amount_in_satoshi = btc_client.to_satoshi(280)
    # # Without any additional params
    # tx_id = await btc_client.send(private_key, to_address, amount_in_satoshi)
    # print(tx_id)

    tx_id = await btc_client.speed_up_transaction_by_self_child_payment(private_key,
                                                                        "dea64fb299ea06975a74d460c1515c689df40d4878f0579af9b20cb987032e62")
    print(tx_id)
    # # Deduct fee from client
    # tx_id = await ltc_client.send(
    #     private_key, to_address, amount_in_satoshi, deduct_fee=True
    # )
    # print(tx_id)
    # tx_id = await ltc_client.send_bulk(
    #     private_key,
    #     {
    #         to_address: amount_in_satoshi,
    #         "tltc1qswslzcdulvlk62gdrg8wa0sw36f938h2cvtaf7": amount_in_satoshi,
    #     },
    # )
    # print(tx_id)
    # balance = await ltc_client.get_balance(
    #     "tltc1qekukv0c9frj3zz8jyag863p8gvv7m3gy2np88d"
    # )
    # print("balance is:", balance)


asyncio.run(main())
