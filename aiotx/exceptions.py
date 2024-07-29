class AioTxError(Exception):
    """
    Base exception for all aiotx errors.
    """


class BlockNotFoundError(AioTxError):
    pass


class BlockMonitoringError(AioTxError):
    pass


class InternalJSONRPCError(AioTxError):
    pass


class StackLimitReachedError(AioTxError):
    pass


class MethodHandlerCrashedError(AioTxError):
    pass


class ExecutionTimeoutError(AioTxError):
    pass


class NonceTooLowError(AioTxError):
    pass


class FilterNotFoundError(AioTxError):
    pass


class TraceRequestLimitExceededError(AioTxError):
    pass


class TransactionCostExceedsGasLimitError(AioTxError):
    pass


class NetworkError(AioTxError):
    pass


class VMExecutionError(AioTxError):
    pass


class MethodNotFoundError(AioTxError):
    pass


class InvalidRequestError(AioTxError):
    pass


class InvalidArgumentError(AioTxError):
    pass


class BlockRangeLimitExceededError(AioTxError):
    pass


class InternalJSONAioTxError(AioTxError):
    pass


class TransactionNotFound(AioTxError):
    pass


class ReplacementTransactionUnderpriced(AioTxError):
    pass


class WrongPrivateKey(AioTxError):
    pass


class InsufficientFunds(AioTxError):
    pass


class RpcConnectionError(AioTxError):
    pass


class CreateTransactionError(AioTxError):
    pass


class NotImplementedError(AioTxError):
    pass
