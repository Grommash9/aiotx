import asyncio

from aiotx.clients import AioTxTONClient
from aiotx.utils.tonsdk.contract.wallet import WalletVersionEnum

# For bulk send we should use HighloadWalletV2Contract and deploy it before the first send!

ton_client = AioTxTONClient(
    "https://testnet.toncenter.com/api/v2",
    workchain=0,
    wallet_version=WalletVersionEnum.hv2,
)

# jetton_wallet_address = asyncio.run(
#     ton_client.get_jetton_wallet_address(
#         "0QDlTHD4T79EyT96gkYNKd3iuRd2__6gGh2PCKpU57jSWbVp", "kQAiboDEv_qRrcEdrYdwbVLNOXBHwShFbtKGbQVJ2OKxY_Di"
#     )
# )

# print("jetton_wallet_address", jetton_wallet_address)

balance = asyncio.run(
    ton_client.get_jetton_wallet_balance(
        "0QAEhA1CupMp7uMOUfHHoh7sqAMNu1xQOydf8fQf-ATpkbpT",
        "kQAiboDEv_qRrcEdrYdwbVLNOXBHwShFbtKGbQVJ2OKxY_Di",
    )
)

print("balance", balance)
