from enum import Enum


class BlockParam(Enum):
    LATEST = "latest"
    EARLIEST = "earliest"
    PENDING = "pending"
    SAFE = "safe"
    FINALIZED = "finalized"


class Wallet:
    def __init__(self) -> None:
        pass
