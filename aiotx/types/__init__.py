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
