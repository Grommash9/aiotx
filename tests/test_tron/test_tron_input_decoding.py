import pytest


@pytest.mark.parametrize(
    "input_data, expected_output",
    [
        ("0x", {"function_name": None, "parameters": None}),
        (
            "0xa9059cbb0000000000000000000000006c793170e99d7b0eb1d3622a8629c5964df96ee70000000000000000000000000000000000000000000000000000000000000064",
            {
                "function_name": "transfer",
                "parameters": {
                    "_to": "0x6c793170e99d7b0eb1d3622a8629c5964df96ee7",
                    "_value": 100,
                },
            },
        ),
        (
            "0xa9059cbb000000000000000000000000f71fd0050238a4d9a6ea8e1ce82c9f2c029a645900000000000000000000000000000000000000000000000000000000004c5ec8",
            {
                "function_name": "transfer",
                "parameters": {
                    "_to": "0xf71fd0050238a4d9a6ea8e1ce82c9f2c029a6459",
                    "_value": 5005000,
                },
            },
        ),
        ("0x12345678", {"function_name": None, "parameters": None}),
    ],
)
def test_decode_transaction_input(tron_client, input_data, expected_output):
    result = tron_client.decode_transaction_input(input_data)
    assert result == expected_output
