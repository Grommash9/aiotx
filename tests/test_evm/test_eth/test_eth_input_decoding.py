import pytest


@pytest.mark.parametrize(
    "input_data, expected_output",
    [
        ("0x", {"function_name": None, "parameters": None}),
        (
            "0xa9059cbb00000000000000000000000012345678901234567890123456789012345678900000000000000000000000000000000000000000000000000000000000000064",
            {
                "function_name": "transfer",
                "parameters": {
                    "_to": "0x1234567890123456789012345678901234567890",
                    "_value": 100,
                },
            },
        ),
        (
            "0x095ea7b3000000000000000000000000098765432109876543210987654321098765432100000000000000000000000000000000000000000000000000000000000003e8",
            {
                "function_name": "approve",
                "parameters": {
                    "_spender": "0x0987654321098765432109876543210987654321",
                    "_value": 1000,
                },
            },
        ),
        (
            "0x23b872dd000000000000000000000000111111111111111111111111111111111111111100000000000000000000000022222222222222222222222222222222222222220000000000000000000000000000000000000000000000000000000000001388",
            {
                "function_name": "transferFrom",
                "parameters": {
                    "_from": "0x1111111111111111111111111111111111111111",
                    "_to": "0x2222222222222222222222222222222222222222",
                    "_value": 5000,
                },
            },
        ),
        ("0x12345678", {"function_name": None, "parameters": None}),
    ],
)
def test_decode_transaction_input(eth_client, input_data, expected_output):
    result = eth_client.decode_transaction_input(input_data)
    assert result == expected_output
