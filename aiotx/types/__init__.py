from dataclasses import dataclass, asdict
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

from enum import Enum

class TronContractType(Enum):
    # https://github.com/tronprotocol/protocol/tree/master/core/contract

    # Account Management
    ACCOUNT_CREATE = "AccountCreateContract"
    ACCOUNT_UPDATE = "AccountUpdateContract"
    SET_ACCOUNT_ID = "SetAccountIdContract"
    ACCOUNT_PERMISSION_UPDATE = "AccountPermissionUpdateContract"

    # Asset Operations
    TRANSFER = "TransferContract"
    TRANSFER_ASSET = "TransferAssetContract"
    ASSET_ISSUE = "AssetIssueContract"
    UNFREEZE_ASSET = "UnfreezeAssetContract"
    UPDATE_ASSET = "UpdateAssetContract"
    PARTICIPATE_ASSET_ISSUE = "ParticipateAssetIssueContract"

    # Resource Management
    FREEZE_BALANCE = "FreezeBalanceContract"
    UNFREEZE_BALANCE = "UnfreezeBalanceContract"
    WITHDRAW_BALANCE = "WithdrawBalanceContract"
    FREEZE_BALANCE_V2 = "FreezeBalanceV2Contract"
    UNFREEZE_BALANCE_V2 = "UnfreezeBalanceV2Contract"
    WITHDRAW_EXPIRE_UNFREEZE = "WithdrawExpireUnfreezeContract"
    DELEGATE_RESOURCE = "DelegateResourceContract"
    UNDELEGATE_RESOURCE = "UnDelegateResourceContract"
    CANCEL_ALL_UNFREEZE_V2 = "CancelAllUnfreezeV2Contract"

    # Storage Operations
    BUY_STORAGE = "BuyStorageContract"
    BUY_STORAGE_BYTES = "BuyStorageBytesContract"
    SELL_STORAGE = "SellStorageContract"
    UPDATE_BROKERAGE = "UpdateBrokerageContract"

    # Smart Contract Operations
    CREATE_SMART_CONTRACT = "CreateSmartContract"
    TRIGGER_SMART_CONTRACT = "TriggerSmartContract"
    CLEAR_ABI_CONTRACT = "ClearABIContract"
    UPDATE_SETTING_CONTRACT = "UpdateSettingContract"
    UPDATE_ENERGY_LIMIT = "UpdateEnergyLimitContract"

    # Exchange Operations
    EXCHANGE_CREATE = "ExchangeCreateContract"
    EXCHANGE_INJECT = "ExchangeInjectContract"
    EXCHANGE_WITHDRAW = "ExchangeWithdrawContract"
    EXCHANGE_TRANSACTION = "ExchangeTransactionContract"

    # Market Operations
    MARKET_SELL_ASSET = "MarketSellAssetContract"
    MARKET_CANCEL_ORDER = "MarketCancelOrderContract"

    # Proposal Operations
    PROPOSAL_CREATE = "ProposalCreateContract"
    PROPOSAL_APPROVE = "ProposalApproveContract"
    PROPOSAL_DELETE = "ProposalDeleteContract"

    # Witness Operations
    WITNESS_CREATE = "WitnessCreateContract"
    WITNESS_UPDATE = "WitnessUpdateContract"
    VOTE_WITNESS = "VoteWitnessContract"

    # Shield Operations
    SHIELDED_TRANSFER = "ShieldedTransferContract"

    # Voting Operations
    VOTE_ASSET = "VoteAssetContract"

class ResourceType(Enum):
    BANDWIDTH = "BANDWIDTH"
    ENERGY = "ENERGY"

@dataclass
class DecodedContractParameters:
    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class DecodedContractPayload:
    contract_type: TronContractType
    parameters: None


@dataclass
class UnDelegateResourceContractParameters(DecodedContractParameters):
    # https://github.com/tronprotocol/protocol/blob/master/core/contract/balance_contract.proto#L109
    owner_address: str
    receiver_address: str
    balance: int
    resource: ResourceType 


@dataclass
class TransferAssetContractParameters(DecodedContractParameters):
    # https://github.com/tronprotocol/protocol/blob/master/core/contract/asset_issue_contract.proto#L36
    owner_address: str
    to_address: str
    asset_name: str
    amount: int

