import asyncio
import logging
import os

import pytest
import vcr
from pytest import FixtureRequest

from aiotx.clients import (
    AioTxBSCClient,
    AioTxBTCClient,
    AioTxETHClient,
    AioTxLTCClient,
    AioTxPolygonClient,
    AioTxTONClient,
    AioTxTRONClient,
)
from aiotx.log import set_logger_level
from aiotx.utils.tonsdk.contract.wallet import WalletVersionEnum

set_logger_level("INFO")

# ALL = "all"
# ANY = "any"
# NEW_EPISODES = "new_episodes"
# NONE = "none"
# ONCE = "once"

BSC_TEST_NODE_URL = "https://bsc-testnet-rpc.publicnode.com"
ETH_TEST_NODE_URL = "https://ethereum-sepolia-rpc.publicnode.com"
LTC_TEST_NODE_URL = "https://api.tatum.io/v3/blockchain/node/litecoin-core-testnet/t-66b98fa76a2e46001c79a063-6be61af199b34129a4797ed2/"
BTC_TEST_NODE_URL = "https://api.tatum.io/v3/blockchain/node/bitcoin-testnet/t-66b98fa76a2e46001c79a063-eecc770265e8462e806b601f/"
TON_MAINNET_NODE_URL = "https://go.getblock.io/875fb0dee2544bb0bc59dd08c6f39330"
POLYGON_TEST_NODE_URL = "https://polygon-amoy-bor-rpc.publicnode.com"
TON_TEST_NODE_URL = "https://testnet.toncenter.com/api/v2"
TRON_TEST_NODE_URL = "https://api.shasta.trongrid.io"

pytest.mark.mysql = pytest.mark.mysql
logging.getLogger("vcr").setLevel(logging.WARNING)
vcr_c = vcr.VCR(
    cassette_library_dir="tests/fixtures/cassettes",
    record_mode=os.environ.get("VCR_RECORD_MODE", "none"),
    match_on=["host", "path", "method", "query", "raw_body", "body"],
    filter_headers=["Authorization", "Cookie", "Date", "X-API-Key"],
)


@pytest.fixture
def ton_client() -> AioTxTONClient:
    # current test rpc connection returning -1 as workchain but it should be 0,
    # so we are setting that param by ourself
    return AioTxTONClient(TON_TEST_NODE_URL, workchain=0)


@pytest.fixture
def ton_mainnet_client() -> AioTxTONClient:
    # testnet block monitoring is not working as
    # expected, and we using mainnet to test monitoring
    return AioTxTONClient(TON_MAINNET_NODE_URL)


@pytest.fixture
def ton_testnet_client_with_hv_wallet() -> AioTxTONClient:
    # testnet block monitoring is not working as
    # expected, and we using mainnet to test monitoring
    return AioTxTONClient(
        TON_TEST_NODE_URL, workchain=0, wallet_version=WalletVersionEnum.hv2
    )


@pytest.fixture
def tron_client() -> AioTxTRONClient:
    return AioTxTRONClient(TRON_TEST_NODE_URL)


@pytest.fixture
def bsc_client() -> AioTxBSCClient:
    return AioTxBSCClient(BSC_TEST_NODE_URL)


@pytest.fixture
def polygon_client() -> AioTxPolygonClient:
    return AioTxPolygonClient(POLYGON_TEST_NODE_URL)


@pytest.fixture
def eth_client() -> AioTxETHClient:
    return AioTxETHClient(ETH_TEST_NODE_URL)


@pytest.fixture
@vcr_c.use_cassette("ltc/create_client.yaml")
def ltc_public_client(request: FixtureRequest) -> AioTxLTCClient:
    def teardown():
        try:
            os.remove("test_ltc.sqlite")
        except FileNotFoundError:
            print("test_ltc.sqlite FileNotFoundError")

    request.addfinalizer(teardown)
    return AioTxLTCClient(
        LTC_TEST_NODE_URL, testnet=True, db_url="sqlite+aiosqlite:///test_ltc.sqlite"
    )


@pytest.fixture
@vcr_c.use_cassette("btc/create_client.yaml")
def btc_client(request: FixtureRequest) -> AioTxBTCClient:
    def teardown():
        try:
            os.remove("test_btc.sqlite")
        except FileNotFoundError:
            print("test_btc.sqlite FileNotFoundError")

    request.addfinalizer(teardown)
    return AioTxBTCClient(
        BTC_TEST_NODE_URL, testnet=True, db_url="sqlite+aiosqlite:///test_btc.sqlite"
    )


@pytest.fixture
@vcr_c.use_cassette("btc/create_client_mysql.yaml")
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
@vcr_c.use_cassette("ltc/create_client_mysql.yaml")
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
