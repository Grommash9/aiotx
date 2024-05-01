from aiotx.clients import AioTxBSCClient
import asyncio


client = AioTxBSCClient("https://nameless-flashy-snow.bsc-testnet.quiknode.pro/c54e248a38fb9b7a8b31d84d57c1e41b203ed019/")

bsc_testnet_private_key = "94e6daf15aa076a932cd9f0663da72f8cfc3d3e23c00ef1269104bd904938fcd"
bsc_send_to = "0xf9E35E4e1CbcF08E99B84d3f6FF662Ba4c306b5a"



# print(asyncio.run(client.send_transaction(bsc_testnet_private_key, bsc_send_to, 1000000, 1000000000)))

print(asyncio.run(client.send_token_transaction("94e6daf15aa076a932cd9f0663da72f8cfc3d3e23c00ef1269104bd904938fcd",
                                                "0xf9E35E4e1CbcF08E99B84d3f6FF662Ba4c306b5a",
                                                "0x337610d27c682E347C9cD60BD4b3b107C9d34dDd",
                                                1000000000, 1000000000, 610000)))