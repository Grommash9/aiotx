import os

import pytest
from conftest import vcr_c  # noqa
from vcr.errors import CannotOverwriteExistingCassetteException

from aiotx.clients import AioTxTONClient
from aiotx.exceptions import (
    AioTxError,
    BlockNotFoundError,
    InvalidArgumentError,
    WrongPrivateKey,
)

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


@pytest.mark.parametrize(
    "shard, seqno, expected_exception, tx_data_result",
    [
        (
            2305843009213693952,
            21020822,
            None,
            {"AwDwEqG+/w64ca+Xoc4JkJl+Iwkrs79Sjs82L2s0Vtw=", "HrT5S8S4zMifwDVspjEKDlSsry/6Nt9IAqmRPnWHdGU="},
        ),
        (
            6917529027641081856,
            21020817,
            None,
            {"hSF1DmJJgbs/o6d9ZoGxoafRBuKChD9DEFNsXVkCQGA="},
        ),
        (
            2305843009213693952,
            21020824,
            None,
            {},
        ),
        (
            2305843009213693952,
            21023867,
            None,
            {"UB4KXyYA5m7cAgQD0UM50AfNhyGCQ2gAsyYyJxrlurI=", "bW6gqpLzLK+cvbiNsd9Njlsrvz7XlJXW2EpUAEV2/dU="},
        ),
        (
            -6917529027641081856,
            21021183,
            None,
            {},
        ),
        (
            78568658568,
            0,
            BlockNotFoundError,
            {},
        ),
    ],
)
@vcr_c.use_cassette("ton/get_block_transactions.yaml")
async def test_get_block_transactions(ton_client: AioTxTONClient, shard, seqno, expected_exception, tx_data_result):
    if expected_exception:
        with pytest.raises(expected_exception):
            await ton_client.get_block_transactions(workchain=0, seqno=seqno, shard=shard, count=2)
    else:
        tx_data = await ton_client.get_block_transactions(workchain=0, seqno=seqno, shard=shard, count=2)
        tx_ids = set([shard["hash"] for shard in tx_data])
        assert tx_ids.symmetric_difference(tx_data_result) == set()


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
    if expected_exception:
        with pytest.raises(expected_exception):
            await ton_client.get_balance(address)
    else:
        balance = await ton_client.get_balance(address)
        assert expected_balance == balance


@pytest.mark.parametrize(
    "address, limit, lt, hash, to_lt, archival, expected_exception, tx_data_result",
    [
        (
            "0QAEhA1CupMp7uMOUfHHoh7sqAMNu1xQOydf8fQf-ATpkbpT",
            None,
            None,
            None,
            None,
            None,
            None,
            {
                "1Uq/leJuBUpMIqvJiziInWLwNKwG6Si4laiK6RBpUKE=",
                "htFdXopqxYctcjLwfOhXMeRRIaAaoSZ9aRnexbfOKg8=",
                "jtaySLcgIPw1siVV7j4h9YFsO+3nex8cW+3wrJ6dGvw=",
                "T168t1RP6sAi8jXYqqir13ErIcfkIPOIyLJ2K3YGX9A=",
            },
        ),
        (
            "0QAEhA1CupMp7uMOUfHHoh7sqAMNu1xQOydf8fQf-ATpkbpT",
            1,
            None,
            None,
            None,
            None,
            None,
            {"htFdXopqxYctcjLwfOhXMeRRIaAaoSZ9aRnexbfOKg8="},
        ),
        (
            "0QAEhA1CupMp7uMOUfHHoh7sqAMNu1xQOydf8fQf-ATpkbpT",
            1,
            22014131000001,
            "htFdXopqxYctcjLwfOhXMeRRIaAaoSZ9aRnexbfOKg8=",
            None,
            None,
            None,
            {"htFdXopqxYctcjLwfOhXMeRRIaAaoSZ9aRnexbfOKg8="},
        ),
        (
            "Ef9fwskZLEuGDfYTRAtvt9k-mEDkaIskkUOsEwPw1wzXk7zR",
            None,
            None,
            None,
            None,
            None,
            InvalidArgumentError,
            {},
        ),
    ],
)
@vcr_c.use_cassette("ton/get_transactions.yaml")
async def test_get_transactions(
    ton_client: AioTxTONClient, address, limit, lt, hash, to_lt, archival, expected_exception, tx_data_result
):
    if expected_exception:
        with pytest.raises(expected_exception):
            await ton_client.get_transactions(address, limit, lt, hash, to_lt, archival)
    else:
        tx_data = await ton_client.get_transactions(address, limit, lt, hash, to_lt, archival)
        tx_ids = set([shard["transaction_id"]["hash"] for shard in tx_data])
        assert tx_ids.symmetric_difference(tx_data_result) == set()


@pytest.mark.parametrize(
    "address, expected_exception, expected_segno",
    [
        (
            "0QAEhA1CupMp7uMOUfHHoh7sqAMNu1xQOydf8fQf-ATpkbpT",
            None,
            2,
        ),
        (
            "EQBsBYu0o3WC4n3ETH6VyuYcjvQPusd4OhG8VIQFELGzgD1y",
            None,
            1,
        ),
        (
            "EQB1mXHwCmSUfwQDLmdsZ7YvY41i8d8clshV52GjL_v0chUj",
            None,
            0,
        ),
        (
            "Ef9fwskZLEuGDfYTRAtvt9k-mEDkaIskkUOsEwPw1wzXk7zR",
            InvalidArgumentError,
            0,
        ),
        (
            "0:6c058bb4a37582e27dc44c7e95cae61c8ef40fbac7783a11bc54840510b1b380",
            None,
            1,
        ),
    ],
)
@vcr_c.use_cassette("ton/get_transaction_count.yaml")
async def test_get_transaction_count(ton_client: AioTxTONClient, address, expected_exception, expected_segno):
    if expected_exception:
        with pytest.raises(expected_exception):
            await ton_client.get_transaction_count(address)
    else:
        transaction_count = await ton_client.get_transaction_count(address)
        assert transaction_count == expected_segno


@pytest.mark.parametrize(
    "address, expected_exception, expected_packed_address",
    [
        (
            "0:95cc5a9ec1eebbbe1265a20dc63cf015d1143f5871b0ae21eeecd0d60cafc74d",
            None,
            "EQCVzFqewe67vhJlog3GPPAV0RQ/WHGwriHu7NDWDK/HTec6",
        ),
        (
            "0:2e80e2e306b9aefaef7e0a00092a31fd6c8d1abc28d9bf4c5a477e65ef817e30",
            None,
            "EQAugOLjBrmu+u9+CgAJKjH9bI0avCjZv0xaR35l74F+MH/3",
        ),
        (
            "0:6c58bb4a37582e27dc44c7e95cae61c8ef40fbac7783a11bc54840510b1b380",
            None,
            "EQAGxYu0o3WC4n3ETH6VyuYcjvQPusd4OhG8VIQFELGzgG2y",
        ),
        (
            "0:6c58bb4a37582e1bc54840510b1b380",
            None,
            "EQAAAAAAAAAAAAAAAAAAAAAABsWLtKN1guG8VIQFELGzgOMO",
        ),
        (
            "0QAEhA1CupMp7uMOUfHHoh7sqAMNu1xQOydf8fQf+ATpkbpT",
            None,
            "0QAEhA1CupMp7uMOUfHHoh7sqAMNu1xQOydf8fQf+ATpkbpT",
        ),
    ],
)
@vcr_c.use_cassette("ton/pack_address.yaml")
async def test_pack_address(ton_client: AioTxTONClient, address, expected_exception, expected_packed_address):
    if expected_exception:
        with pytest.raises(expected_exception):
            await ton_client.pack_address(address)
    else:
        packed_address = await ton_client.pack_address(address)
        assert packed_address == expected_packed_address


@pytest.mark.parametrize(
    "mnemonics_str, expected_address, expected_raw_address, expected_exception",
    [
        (
            "current worth mimic divert pigeon minor scale abstract bicycle usage talent basic zoo merit melt provide old burger lazy actual amazing drop deposit wink",
            "UQC1-T84mX2mz0gWO-o5ND_mL_aPI1CvgUPQBeXFgVCURVBO",
            "0:b5f93f38997da6cf48163bea39343fe62ff68f2350af8143d005e5c581509445",
            None,
        ),
        (
            "motion churn become nest fault bag clog double please soap damage hen steak nerve letter captain purpose flight aerobic fossil butter asthma hole humble",
            "UQDTd43t-plROumWFwPIeSinJwwaPSatt-ZKbIJzaqlge2tD",
            "0:d3778dedfa99513ae9961703c87928a7270c1a3d26adb7e64a6c82736aa9607b",
            None,
        ),
        (
            "collect maze rough ahead viable upgrade resemble music predict flag movie vocal razor multiply cactus describe host admit battle doctor soldier hungry defy decorate",
            "UQCLeN7G4DNOOTw09ODzLmyfEawMhM1lY5PDga0wbAWBI44G",
            "0:8b78dec6e0334e393c34f4e0f32e6c9f11ac0c84cd656393c381ad306c058123",
            None,
        ),
        (
            "elevator shoulder movie quick rural crime portion pumpkin cattle twenty sound force split example cabbage pen moment curious bitter help attend ocean connect",
            "None",
            "EQAAAAAAAAAAAAAAAAAAAAAABsWLtKN1guG8VIQFELGzgOMO",
            WrongPrivateKey,
        ),
        (["elevator", "wot"], "None", "0QAEhA1CupMp7uMOUfHHoh7sqAMNu1xQOydf8fQf+ATpkbpT", AssertionError),
    ],
)
@vcr_c.use_cassette("ton/get_address_from_mnemonics.yaml")
async def test_get_address_from_mnemonics(
    ton_client: AioTxTONClient, mnemonics_str, expected_address, expected_raw_address, expected_exception
):
    if expected_exception:
        with pytest.raises(expected_exception):
            await ton_client.get_address_from_mnemonics(mnemonics_str)
    else:
        urlsafe_address, raw_address = await ton_client.get_address_from_mnemonics(mnemonics_str)
        assert urlsafe_address == expected_address
        assert raw_address == expected_raw_address


@pytest.mark.xfail(raises=CannotOverwriteExistingCassetteException, reason="boc is always new, we can't test it by VCR")
@vcr_c.use_cassette("ton/send_ton_with_custom_seqno.yaml")
async def test_send_ton(ton_client: AioTxTONClient):
    _, address = await ton_client.get_address_from_mnemonics(TON_TEST_WALLET_MEMO)
    tx_count = await ton_client.get_transaction_count(address)
    amount_in_nano = ton_client.to_nano(0.00001)
    result_tx_id = await ton_client.send(TON_TEST_WALLET_MEMO, "UQDU1hdX6SeHmrvzvyjIrLEWUAdJUJar2sw8haIuT_5n-FLh", amount_in_nano, seqno=tx_count)
    assert result_tx_id == "GxXCUERZwia9JbvEyb5aqHoaTXdkbk/5R+Kel8tqsjw="


@pytest.mark.xfail(raises=CannotOverwriteExistingCassetteException, reason="boc is always new, we can't test it by VCR")
@vcr_c.use_cassette("ton/send_ton_with_auto_seqno.yaml")
async def test_send_ton_with_auto_seqno(ton_client: AioTxTONClient):
    amount_in_nano = ton_client.to_nano(0.00001)
    result_tx_id = await ton_client.send(TON_TEST_WALLET_MEMO, "UQDU1hdX6SeHmrvzvyjIrLEWUAdJUJar2sw8haIuT_5n-FLh", amount_in_nano)
    assert result_tx_id == "aJWE/d/toIz8a3vKut952phyEySylxrKFlqg49qDlQA="