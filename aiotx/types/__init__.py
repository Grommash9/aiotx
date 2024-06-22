from dataclasses import dataclass
from enum import Enum


class BlockParam(Enum):
    LATEST = "latest"
    EARLIEST = "earliest"
    PENDING = "pending"
    SAFE = "safe"
    FINALIZED = "finalized"


class FeeEstimate(Enum):
    UNSET = "UNSET"
    ECONOMICAL = "ECONOMICAL"
    CONSERVATIVE = "CONSERVATIVE"


@dataclass
class UTXOType:
    tx_id: str
    output_n: int
    address: str
    amount_satoshi: int
    used: bool
