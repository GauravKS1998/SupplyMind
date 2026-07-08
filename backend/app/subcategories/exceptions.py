from app.exceptions.common import (
    NotFoundException,
    AlreadyExistsException,
)


class SubCategoryNotFoundException(NotFoundException):
    pass


class SubCategoryAlreadyExistsException(AlreadyExistsException):
    pass
