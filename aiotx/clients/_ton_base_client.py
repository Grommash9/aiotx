"https://go.getblock.io/3ea060ad138b45b788f72902e3cf9b38"

# ACCESS_TOKEN = "3ea060ad138b45b788f72902e3cf9b38"

# # getting master block
# curl --location --request GET 'https://go.getblock.io/3ea060ad138b45b788f72902e3cf9b38/getMasterchainInfo'

# # {"ok":true,"result":{"@type":"blocks.masterchainInfo","last":{"@type":"ton.blockIdExt","workchain":-1,"shard":"-9223372036854775808","seqno":38016643,"root_hash":"qe2QTVuhQDOYLNPK2yFxl9nGAsrQ4EY6VVSZn89m6dQ=","file_hash":"p8q63ShU6mOoMR7WX4TB4kXlKlefazFQknWFoMJDiTE="},"state_root_hash":"sRL+rhk/qXpzDweLFEC41+XseK7AScl82e93uLRgpOo=","init":{"@type":"ton.blockIdExt","workchain":-1,"shard":"0","seqno":0,"root_hash":"F6OpKZKqvqeFp6CQmFomXNMfMj2EnaUSOXN+Mh+wVWk=","file_hash":"XplPz01CXAps5qeSWUtxcyBfdAo5zVb1N979KLSKD24="},"@extra":"1716355541.08875:0:0.024924086702997283"}}

# # Getting master block shard blocks
# curl --location --request GET 'https://go.getblock.io/3ea060ad138b45b788f72902e3cf9b38/shards?seqno=38016929' 

# # Getting shard transactions
# curl --location --request GET 'https://go.getblock.io/3ea060ad138b45b788f72902e3cf9b38/getBlockTransactions?workchain=0&shard=2305843009213693952&seqno=43657559&root_hash=NwhUKuaOJjGeej2DpfKjVTbpL87ED7tlaTafV1eMq2o=&count=5' 

# # Get transactions for address (should include block data to get it for that block only? new ones?)
# curl --location --request GET 'https://go.getblock.io/3ea060ad138b45b788f72902e3cf9b38/getTransactions?address=0:272d1e92e231b278f46b89839c6b22fc0bd8e387b35617f298c1d3ae2eb11d5b&limit=2&hash=40ZmLlSKi/WI0xO8TkXpn7RNscnvKSWPQSwt2HE1poQ=' 


# from tonsdk.contract.wallet import WalletVersionEnum, Wallets
# from tonsdk.utils import bytes_to_b64str
# from tonsdk.crypto import mnemonic_new


# wallet_workchain = 0
# wallet_version = WalletVersionEnum.v3r2
# wallet_mnemonics = mnemonic_new()

# _mnemonics, _pub_k, _priv_k, wallet = Wallets.from_mnemonics(
#     wallet_mnemonics, wallet_version, wallet_workchain)
# query = wallet.create_init_external_message()
# base64_boc = bytes_to_b64str(query["message"].to_boc(False))

# print("""
# Mnemonic: {}

# Raw address: {}

# Bounceable, url safe, user friendly address: {}

# Base64boc to deploy the wallet: {}
# """.format(wallet_mnemonics,
#            wallet.address.to_string(),
#            wallet.address.to_string(True, True, True),
#            base64_boc))


# # # Get transactions for address (should include block data to get it for that block only? new ones?)
# curl --location --request GET 'https://go.getblock.io/3ea060ad138b45b788f72902e3cf9b38/getTransactions?address=0:272d1e92e231b278f46b89839c6b22fc0bd8e387b35617f298c1d3ae2eb11d5b&limit=2&hash=40ZmLlSKi/WI0xO8TkXpn7RNscnvKSWPQSwt2HE1poQ=' 

# curl --location --request POST 'https://go.getblock.io/3ea060ad138b45b788f72902e3cf9b38/rest/sendBoc' --header 'Content-Type: application/json' --data-raw '{te6cckECAwEAAQ8AAt+IAJ9vK4gUqMCLXKsssfAigLozwwqp2s5GmDp+L8IV9hqSEYCU4fhOUIzrySDjgJo2xfUQUb2iGmUG5UZmecQphuYEjpEV6wKfEX9vX6/SkVaiIQ5Id+QTma2VfiE+eG4L74AlNTRi/////+AAAAAQAQIA3v8AIN0gggFMl7ohggEznLqxn3Gw7UTQ0x/THzHXC//jBOCk8mCDCNcYINMf0x/TH/gjE7vyY+1E0NMf0x/T/9FRMrryoVFEuvKiBPkBVBBV+RDyo/gAkyDXSpbTB9QC+wDo0QGkyMsfyx/L/8ntVABQAAAAACmpoxc9NEcRRhiEkbrH0HlAcR/tey8wfzgh5UEU+wWBpfLpOODwubg=}'

# curl --location --request POST 'https://go.getblock.io/3ea060ad138b45b788f72902e3cf9b38/jsonRPC' --data-raw {"jsonrpc": "2.0", "method": "getConsensusBlock", "id": "getblock.io"}


# curl --location --request POST 'https://go.getblock.io/3ea060ad138b45b788f72902e3cf9b38/jsonRPC' --header 'Content-Type: application/json' --data-raw '{"jsonrpc": "2.0", "method": "sendBoc", "id": "getblock.io", "boc": "asdasd"}'



# curl --location --request POST 'https://go.getblock.io/3ea060ad138b45b788f72902e3cf9b38/rest//sendBocReturnHash?' --header 'Content-Type: application/json' --data-raw {}


# curl --location --request POST 'https://go.getblock.io/3ea060ad138b45b788f72902e3cf9b38/jsonRPC' --header 'Content-Type: application/json' --data-raw '{"jsonrpc": "2.0", "method": "sendBoc", "id": "getblock.io", "params": {"boc": "te6cckECAwEAAQ8AAt+IAJ9vK4gUqMCLXKsssfAigLozwwqp2s5GmDp+L8IV9hqSEYCU4fhOUIzrySDjgJo2xfUQUb2iGmUG5UZmecQphuYEjpEV6wKfEX9vX6/SkVaiIQ5Id+QTma2VfiE+eG4L74AlNTRi/////+AAAAAQAQIA3v8AIN0gggFMl7ohggEznLqxn3Gw7UTQ0x/THzHXC//jBOCk8mCDCNcYINMf0x/TH/gjE7vyY+1E0NMf0x/T/9FRMrryoVFEuvKiBPkBVBBV+RDyo/gAkyDXSpbTB9QC+wDo0QGkyMsfyx/L/8ntVABQAAAAACmpoxc9NEcRRhiEkbrH0HlAcR/tey8wfzgh5UEU+wWBpfLpOODwubg="}}'