import asyncio

import pytest
from conftest import vcr_c

from aiotx.clients import AioTxBTCClient


@pytest.mark.mysql
@vcr_c.use_cassette("btc/test_async_monitoring_mysql.yaml")
async def test_async_monitoring_mysql(btc_client_mysql: AioTxBTCClient):
    blocks = []
    transactions = []

    @btc_client_mysql.monitor.on_block
    async def handle_block(block):
        blocks.append(block)

    @btc_client_mysql.monitor.on_transaction
    async def handle_transaction(transaction):
        transactions.append(transaction)

    await btc_client_mysql.import_address("tb1pmuuv2qjujv9qawqcc424nhlnmux7mvsyqj7qgc6z0vwqujvx4k9s34kuxn", 2811502)
    await btc_client_mysql.import_address("tb1putn7zkfjr97xd77as09w5syy3x7xr5crp99wycjcxgdwrq3le9lse9fdkd")
    await btc_client_mysql.import_address("tb1p2z70my9zwxsuqevdxjn909c7jyp89z4qv3uhy5wggn47ruvfa65s4fnngd")
    await btc_client_mysql.import_address("tb1paf6damf5052arl3r2lsufuhyu48yth8mrgxdtqj9pervz624q6xqxm7ew3")
    await btc_client_mysql.monitor._add_new_utxo(
        "tb1paf6damf5052arl3r2lsufuhyu48yth8mrgxdtqj9pervz624q6xqxm7ew3",
        "8b88ebe1d0bb1eda7b1512853e75d3884b99e6634317589b1f7457ab92f1e41f",
        499824213,
        0,
    )
    start_balance_utxo_wallet = await btc_client_mysql.get_balance(
        "tb1paf6damf5052arl3r2lsufuhyu48yth8mrgxdtqj9pervz624q6xqxm7ew3"
    )
    assert start_balance_utxo_wallet == 499824213
    await btc_client_mysql.start_monitoring()

    try:
        await asyncio.sleep(4)
    except KeyboardInterrupt:
        btc_client_mysql.stop_monitoring()

    assert len(blocks) > 0
    assert len(transactions) > 0

    assert 2811502 in blocks
    assert 2811503 in blocks
    assert 2811504 in blocks

    # Checking we have all tb1putn7zkfjr97xd77as09w5syy3x7xr5crp99wycjcxgdwrq3le9lse9fdkd transaction
    assert "3f419799747dc83a33a84a8d58fe5e9265d9d1b9b122de6914eb849abb04d9ae" in [tx["txid"] for tx in transactions]
    assert "45fabc1d7bb2b1255d78a00e1daebe37ed855b7965fbae6732bf0624e426d30d" in [tx["txid"] for tx in transactions]
    assert "6643bcac7025154b1ad35d92da73acf7dc51df5d80fab23d9734b07600d8b615" in [tx["txid"] for tx in transactions]

    # tb1p2z70my9zwxsuqevdxjn909c7jyp89z4qv3uhy5wggn47ruvfa65s4fnngd transactions
    assert "c5ff30d25de95338bc4436c6fd49ce35bf74297671f9d0a5a8d52b5022623cc7" in [tx["txid"] for tx in transactions]
    assert "1eb37d5cbad786b6c2954b5d6f69df62a7294a13d068a1393ce4869f61c8b293" in [tx["txid"] for tx in transactions]

    # tb1pmuuv2qjujv9qawqcc424nhlnmux7mvsyqj7qgc6z0vwqujvx4k9s34kuxn transaction
    assert "56f677b37c44f9609f6d2ee121effe5a59b0c550c9be5073d03d8c365dde0e83" in [tx["txid"] for tx in transactions]
    assert "0cfe0b554f766ed374a426497a9163a3beb9732e799ffa623894efaea81a4415" in [tx["txid"] for tx in transactions]
    assert "5f8c9b318ab9156598d3d04701c08f374832bb1ce8704e629a68961b08d290c1" in [tx["txid"] for tx in transactions]
    assert "a9bfc94a0a5d7e7e46f1626b9d1848da96cc85689528ca3187e55164be8f3d04" in [tx["txid"] for tx in transactions]


    balance = await btc_client_mysql.get_balance("tb1pmuuv2qjujv9qawqcc424nhlnmux7mvsyqj7qgc6z0vwqujvx4k9s34kuxn")
    utxo = await btc_client_mysql.monitor._get_utxo_data("tb1pmuuv2qjujv9qawqcc424nhlnmux7mvsyqj7qgc6z0vwqujvx4k9s34kuxn")
    utxo_tx_id_list = [tx[0] for tx in utxo]
    assert "0cfe0b554f766ed374a426497a9163a3beb9732e799ffa623894efaea81a4415" in utxo_tx_id_list
    assert "56f677b37c44f9609f6d2ee121effe5a59b0c550c9be5073d03d8c365dde0e83" in utxo_tx_id_list
    assert "39169a8dcb800afcd71adbbca93f209d5006eb787c98668e22c0550a8450f202" in utxo_tx_id_list
    assert "5f8c9b318ab9156598d3d04701c08f374832bb1ce8704e629a68961b08d290c1" in utxo_tx_id_list
    assert "a9bfc94a0a5d7e7e46f1626b9d1848da96cc85689528ca3187e55164be8f3d04" in utxo_tx_id_list

    assert balance == 499747253
    
    balance = await btc_client_mysql.get_balance("tb1putn7zkfjr97xd77as09w5syy3x7xr5crp99wycjcxgdwrq3le9lse9fdkd")
    
    assert balance == 36481286

    balance = await btc_client_mysql.get_balance("tb1p2z70my9zwxsuqevdxjn909c7jyp89z4qv3uhy5wggn47ruvfa65s4fnngd")
    utxo = await btc_client_mysql.monitor._get_utxo_data("tb1p2z70my9zwxsuqevdxjn909c7jyp89z4qv3uhy5wggn47ruvfa65s4fnngd")
    assert balance == 478778279

    end_balance_utxo_wallet = await btc_client_mysql.get_balance(
        "tb1paf6damf5052arl3r2lsufuhyu48yth8mrgxdtqj9pervz624q6xqxm7ew3"
    )
    assert end_balance_utxo_wallet == 0
    

@vcr_c.use_cassette("btc/test_async_monitoring.yaml")
async def test_async_monitoring(btc_client: AioTxBTCClient):
    blocks = []
    transactions = []

    @btc_client.monitor.on_block
    async def handle_block(block):
        blocks.append(block)

    @btc_client.monitor.on_transaction
    async def handle_transaction(transaction):
        transactions.append(transaction)

    await btc_client.import_address("tb1pmuuv2qjujv9qawqcc424nhlnmux7mvsyqj7qgc6z0vwqujvx4k9s34kuxn", 2811502)
    await btc_client.import_address("tb1putn7zkfjr97xd77as09w5syy3x7xr5crp99wycjcxgdwrq3le9lse9fdkd")
    await btc_client.import_address("tb1p2z70my9zwxsuqevdxjn909c7jyp89z4qv3uhy5wggn47ruvfa65s4fnngd")
    await btc_client.import_address("tb1paf6damf5052arl3r2lsufuhyu48yth8mrgxdtqj9pervz624q6xqxm7ew3")
    await btc_client.monitor._add_new_utxo(
        "tb1paf6damf5052arl3r2lsufuhyu48yth8mrgxdtqj9pervz624q6xqxm7ew3",
        "8b88ebe1d0bb1eda7b1512853e75d3884b99e6634317589b1f7457ab92f1e41f",
        499824213,
        0,
    )
    start_balance_utxo_wallet = await btc_client.get_balance(
        "tb1paf6damf5052arl3r2lsufuhyu48yth8mrgxdtqj9pervz624q6xqxm7ew3"
    )
    assert start_balance_utxo_wallet == 499824213
    await btc_client.start_monitoring()

    try:
        await asyncio.sleep(3)
    except KeyboardInterrupt:
        btc_client.stop_monitoring()

    assert len(blocks) > 0
    assert len(transactions) > 0

    balance = await btc_client.get_balance("tb1pmuuv2qjujv9qawqcc424nhlnmux7mvsyqj7qgc6z0vwqujvx4k9s34kuxn")
    assert balance == 333

    balance = await btc_client.get_balance("tb1putn7zkfjr97xd77as09w5syy3x7xr5crp99wycjcxgdwrq3le9lse9fdkd")
    assert balance == 36731406

    balance = await btc_client.get_balance("tb1p2z70my9zwxsuqevdxjn909c7jyp89z4qv3uhy5wggn47ruvfa65s4fnngd")
    assert balance == 478837110

    end_balance_utxo_wallet = await btc_client.get_balance(
        "tb1paf6damf5052arl3r2lsufuhyu48yth8mrgxdtqj9pervz624q6xqxm7ew3"
    )
    assert end_balance_utxo_wallet == 0

    assert 2811502 in blocks
    assert 2811503 in blocks
    assert "e6eda82369b59c805998fc554f55163d4e4d38f5817adf8c1b6b9f917937bd77" in [tx["txid"] for tx in transactions]
    assert "56f677b37c44f9609f6d2ee121effe5a59b0c550c9be5073d03d8c365dde0e83" in [tx["txid"] for tx in transactions]
