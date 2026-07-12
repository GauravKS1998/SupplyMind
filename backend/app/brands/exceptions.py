from app.exceptions.common import (
    NotFoundException,
    AlreadyExistsException,
    BusinessException,
    InternalServerException,
)


class BrandNotFoundException(NotFoundException):
    pass


class BrandAlreadyExistsException(AlreadyExistsException):
    pass


class BrandInactiveException(BusinessException):
    pass
