from app.exceptions.common import (
    NotFoundException,
    BusinessException,
    InternalServerException,
)


class InvalidTransferRequestException(BusinessException):
    pass


class SourceInventoryNotFoundException(NotFoundException):
    pass


class DestinationInventoryNotFoundException(NotFoundException):
    pass


class InsufficientStockException(BusinessException):
    pass


class TransferFailedException(InternalServerException):
    pass


class TransferNotFoundException(NotFoundException):
    pass


class TransferNotInitiatedException(BusinessException):
    pass


class TransferNotApprovedException(BusinessException):
    pass


class TransferNotInTransitException(BusinessException):
    pass
