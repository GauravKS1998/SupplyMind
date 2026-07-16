from app.exceptions.common import (
    NotFoundException,
    AlreadyExistsException,
    BusinessException,
)


class WarehouseAlreadyExistsException(AlreadyExistsException):
    pass


class WarehouseNotFoundException(NotFoundException):
    pass


class InvalidWarehouseCapacityException(BusinessException):
    pass


class WarehouseCapacityExceededException(BusinessException):
    pass
