from app.exceptions.common import (
    NotFoundException,
    AlreadyExistsException,
)


class WarehouseAlreadyExistsException(AlreadyExistsException):
    pass


class WarehouseNotFoundException(NotFoundException):
    pass
