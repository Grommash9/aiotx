get_transactions
================

.. code-block:: python

    async def get_transactions(
        address, 
        limit: int = None, 
        lt: int = None, 
        hash: str = None, 
        to_lt: int = None, 
        archival: bool = None
    ):

Retrieves transactions for a given TON account.

Parameters:

    - **address** (str): Identifier of the target TON account in any form.
    - **limit** (int, optional): Maximum number of transactions to include in the response. If not specified, the default limit will be used.
    - **lt** (int, optional): Logical time of the transaction to start with. Must be sent together with `hash`. If not specified, the most recent transactions will be returned.
    - **hash** (str, optional): Hash of the transaction to start with, in base64 or hex encoding. Must be sent together with `lt`. If not specified, the most recent transactions will be returned.
    - **to_lt** (int, optional): Logical time of the transaction to finish with. If specified, transactions from `lt` to `to_lt` will be returned.
    - **archival** (bool, optional): If set to `True`, only liteservers with full history will be used to process the request. By default, any available liteserver will be used.

Returns:

    - **list**: A list of dictionaries representing the retrieved transactions.


Example usage:

.. code-block:: python

    address = "EQCc39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2e"
    transactions = await ton_client.get_transactions(
        address, 
        limit=10
        )


In this example, we retrieve the 10 most recent transactions for the specified TON account. The retrieved transactions are then printed, showing the transaction ID, account, logical time, hash, and timestamp for each transaction.


**Response Format**

The `get_transactions` function returns a list of dictionaries, where each dictionary represents a transaction. The structure of each transaction dictionary is as follows:

.. code-block:: python

    {
        "@type": "raw.transaction",
        "address": {
            "@type": "accountAddress",
            "account_address": "EQD_vYX_upIIn1JjpRCuibeosLyLvqfHYQL7cVSk6E3gSxZL"
        },
        "utime": 1716874922,
        "data": "te6cckECCAEAAaoAA7V/+9hf+6kgifUmOlEK6Jt6iwvIu+p8dhAvtxVKToTeBLAAAqh7KylsF7+LIPs3UPK1QNTJoNYDgSVhoMiVN4sGauwSmaGoihTQAAKoeylBJBZlVuqgABRgwY5IAQIDAQGgBACCcnCI2cbJArzfFgcs45EyQV6laeQLFV3Q7hB2fmwD5Z2BmPpZimdKvsix0lklQ0ImvtADJD2mxXqOYPnui2Y5Gg0CFQxAiM4DHBhgwY4RBgcBr0gBILekhv/LaTHG/5RnlgN0ulXlcemGdIsiSeRW8crncckAP+9hf+6kgifUmOlEK6Jt6iwvIu+p8dhAvtxVKToTeBLM4DHABgpzBgAAVQ9lKCSczKrdSMAFAC4AAAAAMTc5NDQxMzcyNzkzNDg5NDA4MwCcQHvoj3wAAAAAAAAAAB0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFvAAAAAAAAAAAAAAAABLUUtpEnlC4z33SeGHxRhIq/htUa7i3D8ghbwxhQTn44ESV9jCg==",
        "transaction_id": {
            "@type": "internal.transactionId",
            "lt": "46762307000001",
            "hash": "uXqQz3LEJjor09cIcZ4IoRQX+IGuVnjBR1zQzut1tKY="
        },
        "fee": "396402",
        "storage_fee": "2",
        "other_fee": "396400",
        "in_msg": {
            "@type": "raw.message",
            "source": "EQCQW9JDf-W0mON_yjPLAbpdKvK49MM6RZEk8it45XO45ECC",
            "destination": "EQD_vYX_upIIn1JjpRCuibeosLyLvqfHYQL7cVSk6E3gSxZL",
            "value": "3673200",
            "fwd_fee": "342403",
            "ihr_fee": "0",
            "created_lt": "46762305000014",
            "body_hash": "JVKtu+ai42U+2U18xF9gaEbhMJE4xjkKKQ9dBZAIlyQ=",
            "msg_data": {
                "@type": "msg.dataText",
                "text": "MTc5NDQxMzcyNzkzNDg5NDA4Mw=="
            },
            "message": "1794413727934894083"
        },
        "out_msgs": []
    }

Note that the actual content and structure of the transaction data may vary depending on the specific transaction type and the TON network.

You can iterate over the list of transactions and access the desired fields from each transaction dictionary to extract the relevant information.