import logging
import os

import pytest
import vcr

from aiotx.clients import AioTxBSCClient, AioTxETHClient

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
    filter_headers=["Authorization", "Cookie"],
    ignore_hosts=["127.0.0.1", "localhost"],
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