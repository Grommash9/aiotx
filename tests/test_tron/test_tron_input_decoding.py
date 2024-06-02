import pytest


@pytest.mark.parametrize(
    "input_data, expected_output",
    [
        ("0x", {"function_name": None, "parameters": None}),
        (
            "a9059cbb0000000000000000000000006c793170e99d7b0eb1d3622a8629c5964df96ee70000000000000000000000000000000000000000000000000000000000000064",
            {
                "function_name": "transfer",
                "parameters": {"_to": "0x6c793170e99d7b0eb1d3622a8629c5964df96ee7", "_value": 100},
            },
        ),
        # (
        #     "a9059cbb000000000000000000000041a99c7a242576a0bc812185bb2a9d1674def1612e0000000000000000000000000000000000000000000000000000000019bfcc00",
        #     {
        #         "function_name": "approve",
        #         "parameters": {"spender": "0x0987654321098765432109876543210987654321", "amount": 1000},
        #     },
        # ),
        ("0x12345678", {"function_name": None, "parameters": None}),
    ],
)
def test_decode_transaction_input(tron_client, input_data, expected_output):
    result = tron_client.decode_transaction_input(input_data)
    assert result == expected_output
