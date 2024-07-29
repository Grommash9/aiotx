import asyncio

from aiotx.clients import AioTxTONClient

ton_client = AioTxTONClient(
    "https://testnet.toncenter.com/api/v2",
    headers={
        "X-API-Key": "c87fbfad07e66b778bffbe20a5183e55e72f0db97bf68bf5e50170cb53fb115b"
    },
)


@ton_client.monitor.on_block
async def handle_block(block):
    # Here we will get master block id after checking all the shards
    print("ton_client: block", block)


@ton_client.monitor.on_transaction
async def handle_transaction(transaction):
    # here we will get transactions in format:
    """
    {'@type': 'blocks.shortTxId', 'mode': 135,
    'account': '0:cba3b0db18b250e86f96dec1526ce6505d0a918a8fc842facfbc490ec3a68be6',
    'lt': '22079497000007', 'hash': 'I05x4IRYx2AIfWG9fSa/E3S5XF8RxW48Gx3QWEl81CI='}
    """
    # If you want to get more details - you should use get transaction function like that:
    """
    tx_details = await ton_client.get_transactions(
        "0:cba3b0db18b250e86f96dec1526ce6505d0a918a8fc842facfbc490ec3a68be6",
        1, 22079497000007, "I05x4IRYx2AIfWG9fSa/E3S5XF8RxW48Gx3QWEl81CI=")
    """
    # We are not getting all details for all the transaction because it will consume a lot of api calls
    print("ton_client: transaction", transaction)


async def main():
    await ton_client.start_monitoring()


if __name__ == "__main__":
    asyncio.run(main())
