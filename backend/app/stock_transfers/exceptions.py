class StockTransfersException(Exception):
    pass


class InvalidTransferRequestException(StockTransfersException):
    pass


class SourceInventoryNotFoundException(StockTransfersException):
    pass


class DestinationInventoryNotFoundException(StockTransfersException):
    pass


class InsufficientStockException(StockTransfersException):
    pass


class TransferFailedException(StockTransfersException):
    pass


class TransferNotFoundException(StockTransfersException):
    pass


class TransferNotInitiatedException(StockTransfersException):
    pass


class TransferNotApprovedException(StockTransfersException):
    pass


class TransferNotInTransitException(StockTransfersException):
    pass
