import asyncio

from aiotx.clients import AioTxETHClient

eth_client = AioTxETHClient(node_url="https://ethereum-sepolia-rpc.publicnode.com")

private_key = "231d9a16df21402be2b2b50343c489129f1d42dcbaa18b553e6c99057e699df6"
USDC_contract = "0x13fA158A117b93C27c55b8216806294a0aE88b6D"
USDT_contract = "0x419Fe9f14Ff3aA22e46ff1d03a73EdF3b70A62ED"
to_address = "0xf9E35E4e1CbcF08E99B84d3f6FF662Ba4c306b5a"

eth_in_wei = eth_client.to_wei(0.00001, "ether")
tokens_in_mwei = eth_client.to_wei(1, "mwei")


async def main():
    nonce = await eth_client.get_transactions_count(to_address)
    tx_id = await eth_client.send(private_key, to_address, eth_in_wei)
    print(tx_id)
    tx_id = await eth_client.send_token(
        private_key, to_address, USDT_contract, tokens_in_mwei, nonce=nonce + 1
    )
    print(tx_id)
    tx_id = await eth_client.send_token(
        private_key, to_address, USDT_contract, tokens_in_mwei, nonce=nonce + 2
    )
    print(tx_id)


asyncio.run(main())
