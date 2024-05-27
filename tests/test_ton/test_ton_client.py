import os

import pytest
from conftest import vcr_c  # noqa

from aiotx.clients import AioTxTONClient
from aiotx.exceptions import BlockNotFoundError, InvalidArgumentError, AioTxError

TON_TEST_WALLET_MEMO = os.environ.get("TON_TEST_WALLET_MEMO")
assert TON_TEST_WALLET_MEMO is not None, "Please provide TON_TEST_WALLET_MEMO"


@vcr_c.use_cassette("ton/get_last_master_block.yaml")
async def test_get_last_master_block(ton_client: AioTxTONClient):
    master_block_data = await ton_client.get_last_master_block()
    assert isinstance(master_block_data, dict)
    for key in ["shard", "workchain", "seqno", "root_hash"]:
        assert key in master_block_data.keys()


@pytest.mark.parametrize(
    "seqno, expected_exception, shards_result",
    [
        (
            19563127,
            None,
            {"2305843009213693952", "6917529027641081856", "-6917529027641081856", "-2305843009213693952"},
        ),
        (
            19563129,
            None,
            {"-2305843009213693952", "-6917529027641081856", "2305843009213693952", "6917529027641081856"},
        ),
        (
            19563128,
            None,
            {"-2305843009213693952", "-6917529027641081856", "2305843009213693952", "6917529027641081856"},
        ),
        (
            19566127,
            None,
            {"-2305843009213693952", "-6917529027641081856", "2305843009213693952", "6917529027641081856"},
        ),
        (
            19563137,
            None,
            {"2305843009213693952", "6917529027641081856", "-6917529027641081856", "-2305843009213693952"},
        ),
        (
            19563227,
            None,
            {"-2305843009213693952", "-6917529027641081856", "2305843009213693952", "6917529027641081856"},
        ),
        (1951663127, BlockNotFoundError, {-2305843009213693952, 6917529027641081856, -2305843009213693952}),
    ],
)
@vcr_c.use_cassette("ton/get_master_block_shards.yaml")
async def test_get_master_block_shards(ton_client: AioTxTONClient, seqno, expected_exception, shards_result):
    if expected_exception:
        with pytest.raises(expected_exception):
            await ton_client.get_master_block_shards(seqno=seqno)
    else:
        shards_data = await ton_client.get_master_block_shards(seqno=seqno)
        shard_numbers = set([shard["shard"] for shard in shards_data])
        assert shard_numbers.symmetric_difference(shards_result) == set()


# @pytest.mark.parametrize(
#     "seqno, shard, expected_exception, tx_data_result",
#     [
#         (
#             2305843009213693952,
#             21020822,
#             None,
#             {"2305843009213693952", "6917529027641081856", "-6917529027641081856", "-2305843009213693952"},
#         ),
#         (
#             6917529027641081856,
#             21020817,
#             None,
#             {"2305843009213693952", "6917529027641081856", "-6917529027641081856", "-2305843009213693952"},
#         ),
#         (
#             2305843009213693952,
#             21020824,
#             None,
#             {"2305843009213693952", "6917529027641081856", "-6917529027641081856", "-2305843009213693952"},
#         ),
#         (
#             2305843009213693952,
#             21023867,
#             None,
#             {"2305843009213693952", "6917529027641081856", "-6917529027641081856", "-2305843009213693952"},
#         ),
#         (
#             -6917529027641081856,
#             21021183,
#             None,
#             {"2305843009213693952", "6917529027641081856", "-6917529027641081856", "-2305843009213693952"},
#         ),
#     ],
# )
# @vcr_c.use_cassette("ton/get_block_transactions.yaml")
# async def test_get_block_transactions(ton_client: AioTxTONClient, seqno, shard, expected_exception, tx_data_result):

#     if expected_exception:
#         with pytest.raises(expected_exception):
#             await ton_client.get_block_transactions(seqno=seqno, shard=shard, count=2)
#     else:
#         tx_data = await ton_client.get_block_transactions(seqno=seqno, shard=shard, count=2)
#         tx_ids = set([shard["hash"] for shard in tx_data])
#         assert tx_ids.symmetric_difference(tx_data_result) == set()


@pytest.mark.parametrize(
    "address, expected_balance, expected_exception",
    [
        (
            "EQDBNfV4DQzSyzNMw6BCTSZSoUi-CzWcYNsfhKxoDqfrwFtS",
            100917944877,
            None,
        ),
        (
            "Ef8jPzrhTYloKgTCsGgEFNx7OdH-sJ98etJnwrIVSsFxH9mu",
            92845495719,
            None,
        ),
        (
            "EQC1ZeKX1LNrlQ4bwi3je3KVM1AoZ3rkeyHM5hv9pYzmIh4v",
            24984729082,
            None,
        ),
        (
            "Ef9fwskZLEuGDfYTRAtvt9k-mEdkaIskkUOsEwPw1wzXk7zR",
            72142761735,
            None,
        ),
        (
            "0:6c058bb4a37582e27dc44c7e95cae61c8ef40fbac7783a11bc54840510b1b380",
            87235995,
            None,
        ),
        (
            "0:6c058bb4a37582e1b380",
            0,
            None,
        ),
        (
            "1:6c058bb4a37582e27dc44c7e95cae61c8ef40fbac7783a11bc54840510b1b380",
            87235995,
            AioTxError,
        ),
        (
            "Ef9fwskZLEuGDfYTRAtvt9k-mEDkaIskkUOsEwPw1wzXk7zR",
            87235995,
            InvalidArgumentError,
        ),
    ],
)
@vcr_c.use_cassette("ton/get_balance.yaml")
async def test_get_balance(ton_client: AioTxTONClient, address, expected_balance, expected_exception):
    import time

    time.sleep(1)
    if expected_exception:
        with pytest.raises(expected_exception):
            await ton_client.get_balance(address)
    else:
        balance = await ton_client.get_balance(address)
        assert expected_balance == balance
