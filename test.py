from aiotx.clients import AioTxBSCClient
import asyncio


client = AioTxBSCClient("https://nameless-flashy-snow.bsc-testnet.quiknode.pro/c54e248a38fb9b7a8b31d84d57c1e41b203ed019/")

print(asyncio.run(client.get_token_balance("0x08265dA01E1A65d62b903c7B34c08cB389bF3D99", "0x337610d27c682E347C9cD60BD4b3b107C9d34dDd")))