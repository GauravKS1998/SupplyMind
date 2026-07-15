from app.exceptions.common import (
    NotFoundException,
    AlreadyExistsException,
    BusinessException,
)


class SubCategoryNotFoundException(NotFoundException):
    pass


class SubCategoryAlreadyExistsException(AlreadyExistsException):
    pass


class SubCategoryInactiveException(BusinessException):
    pass
