import pytest


@pytest.mark.parametrize(
    "input_data, expected_output",
    [
        ("0x", {"function_name": None, "parameters": None}),
        (
            "0xa9059cbb000000000000000000000000f9e35e4e1cbcf08e99b84d3f6ff662ba4c306b5a0000000000000000000000000000000000000000000000015af1d78b58c40000",
            {
                "function_name": "transfer",
                "parameters": {
                    "_to": "0xf9e35e4e1cbcf08e99b84d3f6ff662ba4c306b5a",
                    "_value": 25000000000000000000,
                },
            },
        ),
        (
            "0x095ea7b3000000000000000000000000c03fd5bca10103b7e5032f0bf770395356454f4600000000000000000000000000000000000000000000000d8d726b7177a80000",
            {
                "function_name": "approve",
                "parameters": {
                    "_spender": "0xc03fd5bca10103b7e5032f0bf770395356454f46",
                    "_value": 250000000000000000000,
                },
            },
        ),
        ("0x12345678", {"function_name": None, "parameters": None}),
    ],
)
def test_decode_transaction_input(eth_client, input_data, expected_output):
    result = eth_client.decode_transaction_input(input_data)
    assert result == expected_output
