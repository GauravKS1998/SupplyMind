from app.exceptions.common import (
    NotFoundException,
    AlreadyExistsException,
)


class ProductTypeNotFoundException(NotFoundException):
    pass


class ProductTypeAlreadyExistsException(AlreadyExistsException):
    pass
