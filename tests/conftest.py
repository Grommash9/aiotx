import asyncio
import logging
import os

import pytest
import vcr
from pytest import FixtureRequest

from aiotx.clients import AioTxBSCClient, AioTxBTCClient, AioTxETHClient, AioTxLTCClient

# ALL = "all"
# ANY = "any"
# NEW_EPISODES = "new_episodes"
# NONE = "none"
# ONCE = "once"

pytest.mark.mysql = pytest.mark.mysql
logging.getLogger("vcr").setLevel(logging.WARNING)
vcr_c = vcr.VCR(
    cassette_library_dir="tests/fixtures/cassettes",
    record_mode=os.environ.get("VCR_RECORD_MODE", "none"),
    match_on=["host", "path", "method", "query", "raw_body", "body"],
    filter_headers=["Authorization", "Cookie", "Date"],
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
def ltc_public_client(request: FixtureRequest) -> AioTxLTCClient:
    def teardown():
        try:
            os.remove("test_ltc.sqlite")
        except FileNotFoundError:
            print("test_ltc.sqlite FileNotFoundError")

    request.addfinalizer(teardown)
    return AioTxLTCClient(LTC_TEST_NODE_URL, testnet=True, db_url="sqlite+aiosqlite:///test_ltc.sqlite")


BTC_TEST_NODE_URL = "https://dry-compatible-cloud.btc-testnet.quiknode.pro/268755801856724a0c520053c0bc3b0a7b1a2d3e/"


@pytest.fixture
def btc_client(request: FixtureRequest) -> AioTxBTCClient:
    def teardown():
        try:
            os.remove("test_btc.sqlite")
        except FileNotFoundError:
            print("test_btc.sqlite FileNotFoundError")

    request.addfinalizer(teardown)
    return AioTxBTCClient(BTC_TEST_NODE_URL, testnet=True, db_url="sqlite+aiosqlite:///test_btc.sqlite")


@pytest.fixture
def btc_client_mysql(request: FixtureRequest) -> AioTxBTCClient:
    aiotx_btc_mysql_client = AioTxBTCClient(
        BTC_TEST_NODE_URL,
        testnet=True,
        db_url=f"mysql+aiomysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
    )


    def teardown():
        asyncio.run(aiotx_btc_mysql_client.monitor._drop_tables())

    request.addfinalizer(teardown)
    return aiotx_btc_mysql_client

@pytest.fixture
def ltc_client_mysql(request: FixtureRequest) -> AioTxLTCClient:
    aiotx_ltc_mysql_client = AioTxLTCClient(
        LTC_TEST_NODE_URL,
        testnet=True,
        db_url=f"mysql+aiomysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
    )


    def teardown():
        asyncio.run(aiotx_ltc_mysql_client.monitor._drop_tables())

    request.addfinalizer(teardown)
    return aiotx_ltc_mysql_client