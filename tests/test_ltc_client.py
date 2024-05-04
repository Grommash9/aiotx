from conftest import vcr_c

from aiotx.clients import AioTxLTCClient


@vcr_c.use_cassette("ltc/get_last_block.yaml")
async def test_get_last_block(ltc_public_client: AioTxLTCClient):
    block_id = await ltc_public_client.get_last_block_number()
    assert isinstance(block_id, int)


@vcr_c.use_cassette("ltc/get_last_block_with_auth.yaml")
async def test_get_last_block_with_auth(ltc_client_with_auth: AioTxLTCClient):
    block_id = await ltc_client_with_auth.get_last_block_number()
    assert isinstance(block_id, int)


@vcr_c.use_cassette("ltc/get_block_by_number.yaml")
async def test_get_block_by_number(ltc_public_client: AioTxLTCClient):
    block = await ltc_public_client.get_block_by_number(3247846)
    assert isinstance(block, dict)

    assert block["hash"] == "4314081d2a5d8633c51799113aac1516f174d5da5793c966848ac34177fb61c9"

    tx_hashes = [tx["hash"] for tx in block["tx"]]
    assert "68e73174f7b44edad7289a771d3069ff91c8bbb30cf96ea9861a4a312c1a2dda" in tx_hashes
    assert "4676f0e42c940f827c7f3b580119c10fe282b39bdbb798dc96d9292c387b37f0" in tx_hashes




    