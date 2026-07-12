from app.exceptions.common import (
    NotFoundException,
    AlreadyExistsException,
    BusinessException,
)


class ProductNotFoundException(NotFoundException):
    pass


class ProductAlreadyExistsException(AlreadyExistsException):
    pass


class ProductInactiveException(BusinessException):
    pass
