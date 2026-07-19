from app.exceptions.common import (
    NotFoundException,
    AlreadyExistsException,
    BusinessException,
)


class InventoryNotFoundException(NotFoundException):
    pass


class InventoryAlreadyExistsException(AlreadyExistsException):
    pass


class InvalidInventoryQuantityException(BusinessException):
    pass


class InventoryInactiveException(BusinessException):
    pass


class InvalidReservedQuantityException(BusinessException):
    pass


class InvalidReorderLevelException(BusinessException):
    pass


class InvalidUnitCostException(BusinessException):
    pass


class InvalidInventoryDatesException(BusinessException):
    pass
