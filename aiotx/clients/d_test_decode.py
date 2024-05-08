from binascii import unhexlify
from io import BytesIO


def decode_signed_transaction(signed_transaction):
    transaction_hex = unhexlify(signed_transaction)
    transaction_stream = BytesIO(transaction_hex)

    # Read the transaction version (4 bytes)
    version = int.from_bytes(transaction_stream.read(4), byteorder='little')

    # Read the number of inputs (varint)
    num_inputs = read_varint(transaction_stream)

    # Read the inputs
    inputs = []
    for _ in range(num_inputs):
        prev_tx_hash = transaction_stream.read(32)[::-1].hex()
        prev_tx_index = int.from_bytes(transaction_stream.read(4), byteorder='little')
        script_sig_length = read_varint(transaction_stream)
        script_sig = transaction_stream.read(script_sig_length).hex()
        sequence = int.from_bytes(transaction_stream.read(4), byteorder='little')
        inputs.append({
            'prev_tx_hash': prev_tx_hash,
            'prev_tx_index': prev_tx_index,
            'script_sig': script_sig,
            'sequence': sequence
        })

    # Read the number of outputs (varint)
    num_outputs = read_varint(transaction_stream)

    # Read the outputs
    outputs = []
    for _ in range(num_outputs):
        value = int.from_bytes(transaction_stream.read(8), byteorder='little')
        script_pub_key_length = read_varint(transaction_stream)
        script_pub_key = transaction_stream.read(script_pub_key_length).hex()
        outputs.append({
            'value': value,
            'script_pub_key': script_pub_key
        })

    # Read the locktime (4 bytes)
    locktime = int.from_bytes(transaction_stream.read(4), byteorder='little')

    # Read the witness data (if present)
    witness_data = []
    if transaction_stream.tell() < len(transaction_hex):
        for _ in range(num_inputs):
            num_items = read_varint(transaction_stream)
            items = []
            for _ in range(num_items):
                item_length = read_varint(transaction_stream)
                item = transaction_stream.read(item_length).hex()
                items.append(item)
            witness_data.append(items)

    decoded_transaction = {
        'version': version,
        'inputs': inputs,
        'outputs': outputs,
        'locktime': locktime,
        'witness_data': witness_data
    }

    return decoded_transaction

def read_varint(stream):
    varint = int.from_bytes(stream.read(1), byteorder='little')
    if varint < 0xfd:
        return varint
    elif varint == 0xfd:
        return int.from_bytes(stream.read(2), byteorder='little')
    elif varint == 0xfe:
        return int.from_bytes(stream.read(4), byteorder='little')
    elif varint == 0xff:
        return int.from_bytes(stream.read(8), byteorder='little')
    

print(decode_signed_transaction("020000000132b225f29505be6e676e076e0c8960cc4c080285b2d95e963a005be71455eab60000000000ffffffff0280f0fa02000000001600145551346a80945c3a50fe3c55572b39cafb5b283fe03fee050000000016001483a100f161bcfb3f6d290d1a0eeebe0e8e92589eea0000000001006d02493046022100db2fff268145b3015876a95b2da37c295dd8b80f66ba3abbd12aa2a3a432d77302210080096880d404f153ce01a6a87f966d9af159c6ee0ea025668e09374df723055b0121032483516ae6532dbeaf537cb5c1da64f973a6066fbde788f665b3dbd45f7417a9"))
