from app.exceptions.common import (
    NotFoundException,
    AlreadyExistsException,
    BusinessException,
)


class CategoryNotFoundException(NotFoundException):
    pass


class CategoryAlreadyExistsException(AlreadyExistsException):
    pass


class CategoryInactiveException(BusinessException):
    pass
