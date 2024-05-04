import logging
import os

import pytest
import vcr

from aiotx.clients import AioTxBSCClient, AioTxBTCClient, AioTxETHClient, AioTxLTCClient

# ALL = "all"
# ANY = "any"
# NEW_EPISODES = "new_episodes"
# NONE = "none"
# ONCE = "once"

logging.getLogger("vcr").setLevel(logging.WARNING)
vcr_c = vcr.VCR(
    cassette_library_dir="tests/fixtures/cassettes",
    record_mode=os.environ.get("VCR_RECORD_MODE", "none"),
    match_on=["host", "path", "method", "query", "raw_body", "body"],
    filter_headers=["Authorization", "Cookie"]
)

BSC_TEST_NODE_URL = "https://nameless-flashy-snow.bsc-testnet.quiknode.pro/c54e248a38fb9b7a8b31d84d57c1e41b203ed019/"
BSC_TEST_CHAIN_ID = 97

@pytest.fixture
def bsc_client() -> AioTxBSCClient:
    return AioTxBSCClient(BSC_TEST_NODE_URL, BSC_TEST_CHAIN_ID)


ETH_TEST_NODE_URL = "https://ethereum-sepolia-rpc.publicnode.com"
ETH_TEST_CHAIN_ID = 11155111

@pytest.fixture
def eth_client() -> AioTxETHClient:
    return AioTxETHClient(ETH_TEST_NODE_URL, ETH_TEST_CHAIN_ID)


LTC_TEST_NODE_URL = "https://api.tatum.io/v3/blockchain/node/litecoin-core-testnet"

@pytest.fixture
def ltc_public_client() -> AioTxLTCClient:
    return AioTxLTCClient(LTC_TEST_NODE_URL, testnet=True)


LTC_TEST_NODE_URL_WITH_AUTH = "http://localhost:19332/wallet/main2"
LTC_TEST_NODE_LOGIN = "litecoinrpc"
LTC_TEST_NODE_PASSWORD = os.getenv("LTC_TEST_NODE_PASSWORD")
assert LTC_TEST_NODE_PASSWORD is not None, "Provide LTC_TEST_NODE_PASSWORD"

@pytest.fixture
def ltc_client_with_auth() -> AioTxLTCClient:
    return AioTxLTCClient(LTC_TEST_NODE_URL_WITH_AUTH, node_username=LTC_TEST_NODE_LOGIN, node_password=LTC_TEST_NODE_PASSWORD, testnet=True)

BTC_TEST_NODE_URL = "https://dry-compatible-cloud.btc-testnet.quiknode.pro/268755801856724a0c520053c0bc3b0a7b1a2d3e/"

@pytest.fixture
def btc_client() -> AioTxBTCClient:
    return AioTxBTCClient(BTC_TEST_NODE_URL, testnet=True)
