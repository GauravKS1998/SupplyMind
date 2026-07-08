from app.exceptions.common import (
    NotFoundException,
    AlreadyExistsException,
)


class ProductNotFoundException(NotFoundException):
    pass


class ProductAlreadyExistsException(AlreadyExistsException):
    pass
