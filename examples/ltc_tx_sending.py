import asyncio

from aiotx.clients import AioTxLTCClient

LTC_TEST_NODE_URL = "TESTNET NODE URL"
ltc_client = AioTxLTCClient(LTC_TEST_NODE_URL, testnet=True)


private_key = "18553b3eb4c5f905d7b023e1736b55ffcbf47657d2cb27f398526ddc9d1764e7"
address = "tltc1qekukv0c9frj3zz8jyag863p8gvv7m3gy2np88d"
to_address = "tltc1qswa8y94sd0njs0atf7h2rmr638nuksw0p2m03v"


async def main():
    balance = await ltc_client.get_balance(
        "tltc1qekukv0c9frj3zz8jyag863p8gvv7m3gy2np88d"
    )
    print("balance is:", balance)
    amount_in_satoshi = ltc_client.to_satoshi(0.0005)
    # Without any additional params
    tx_id = await ltc_client.send(private_key, to_address, amount_in_satoshi)
    print(tx_id)
    # Deduct fee from client
    tx_id = await ltc_client.send(
        private_key, to_address, amount_in_satoshi, deduct_fee=True
    )
    print(tx_id)
    tx_id = await ltc_client.send_bulk(
        private_key,
        {
            to_address: amount_in_satoshi,
            "tltc1qswslzcdulvlk62gdrg8wa0sw36f938h2cvtaf7": amount_in_satoshi,
        },
    )
    print(tx_id)
    balance = await ltc_client.get_balance(
        "tltc1qekukv0c9frj3zz8jyag863p8gvv7m3gy2np88d"
    )
    print("balance is:", balance)


asyncio.run(main())
