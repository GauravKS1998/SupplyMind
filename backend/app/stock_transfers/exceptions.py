from app.exceptions.common import (
    NotFoundException,
    BusinessException,
)


class StockTransferNotFoundException(NotFoundException):
    pass


class StockTransferLineNotFoundException(NotFoundException):
    pass


class InvalidStockTransferException(BusinessException):
    pass


class StockTransferNotInitiatedException(BusinessException):
    pass


class StockTransferNotApprovedException(BusinessException):
    pass


class StockTransferNotInTransitException(BusinessException):
    pass


class StockTransferCannotBeCancelledException(BusinessException):
    pass


class SourceInventoryNotFoundException(NotFoundException):
    pass


class InsufficientStockException(BusinessException):
    pass
