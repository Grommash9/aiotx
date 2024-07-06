import asyncio

from aiotx.clients import AioTxTONClient
from aiotx.utils.tonsdk.contract.wallet import WalletVersionEnum

# For bulk send we should use HighloadWalletV2Contract and deploy it before the first send!

ton_client = AioTxTONClient(
    "https://testnet.toncenter.com/api/v2",
    workchain=0,
    wallet_version=WalletVersionEnum.hv2,
)


recipients_list = [
    {
        "address": "0QAEhA1CupMp7uMOUfHHoh7sqAMNu1xQOydf8fQf-ATpkbpT",
        "amount": 1,
        "payload": "Hello, recipient 1!",
        "send_mode": 1,
    },
    {
        "address": "UQDlTHD4T79EyT96gkYNKd3iuRd2__6gGh2PCKpU57jSWQ7j",
        "amount": 10,
        "payload": "Hello, recipient 5!",
        "send_mode": 1,
    },
]

# You should deploy the wallet before you will be able to start using it, wallet should have balance for that to deploy itself!

tx_id = asyncio.run(
    ton_client.deploy_wallet(
        "ancient reason board glue post sea write shrimp feel motion win away pizza sword mobile ethics film lawsuit nephew cloud crash okay hero step"
    )
)

tx_id = asyncio.run(
    ton_client.send_bulk(
        "ancient reason board glue post sea write shrimp feel motion win away pizza sword mobile ethics film lawsuit nephew cloud crash okay hero step",
        recipients_list,
    )
)

print("tx_id", tx_id)
