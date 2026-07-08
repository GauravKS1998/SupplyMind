from app.exceptions.common import (
    NotFoundException,
    AlreadyExistsException,
)


class CategoryNotFoundException(NotFoundException):
    pass


class CategoryAlreadyExistsException(AlreadyExistsException):
    pass
