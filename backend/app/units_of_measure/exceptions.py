from app.exceptions.common import (
    AlreadyExistsException,
    BusinessException,
    NotFoundException,
)


class UnitOfMeasureNotFoundException(NotFoundException):
    pass


class UnitOfMeasureAlreadyExistsException(AlreadyExistsException):
    pass


class UnitOfMeasureInactiveException(BusinessException):
    pass
