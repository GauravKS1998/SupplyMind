from app.exceptions.common import (
    NotFoundException,
    AlreadyExistsException,
)


class InventoryNotFoundException(NotFoundException):
    pass


class InventoryAlreadyExistsException(AlreadyExistsException):
    pass
