from app.exceptions.common import (
    NotFoundException,
    AlreadyExistsException,
    BusinessException,
    InternalServerException,
)


class SalesOrderAlreadyExistsException(AlreadyExistsException):
    pass


class SalesOrderNotFoundException(NotFoundException):
    pass


class SalesOrderNotDraftedException(BusinessException):
    pass


class SalesOrderNotConfirmedException(BusinessException):
    pass


class SalesOrderNotReservedException(BusinessException):
    pass


class SalesOrderNotDispatchedException(BusinessException):
    pass


class SalesOrderNotDeliveredException(BusinessException):
    pass


class SalesOrderCannotBeCancelledException(BusinessException):
    pass


class InsufficientStockException(BusinessException):
    pass


class SalesOrderFailException(InternalServerException):
    pass
