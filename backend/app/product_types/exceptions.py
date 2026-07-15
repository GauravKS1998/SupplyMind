from app.exceptions.common import (
    NotFoundException,
    AlreadyExistsException,
    BusinessException,
)


class ProductTypeNotFoundException(NotFoundException):
    pass


class ProductTypeAlreadyExistsException(AlreadyExistsException):
    pass


class ProductTypeInactiveException(BusinessException):
    pass
