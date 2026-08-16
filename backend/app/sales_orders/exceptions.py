from app.exceptions.common import (
    NotFoundException,
    BusinessException,
)


class SalesOrderNotFoundException(NotFoundException):
    pass


class SalesOrderLineNotFoundException(NotFoundException):

    def __init__(self, sales_order_line_id: int):
        super().__init__(
            f"Sales Order Line with id '{sales_order_line_id}' was not found."
        )


class SalesOrderCannotBeModifiedException(BusinessException):
    pass


class SalesOrderCannotBeConfirmedException(BusinessException):
    pass


class SalesOrderCannotBeReservedException(BusinessException):
    pass


class SalesOrderCannotBeDispatchedException(BusinessException):
    pass


class SalesOrderCannotBeDeliveredException(BusinessException):
    pass


class SalesOrderCannotBeCompletedException(BusinessException):
    pass


class SalesOrderCannotBeCancelledException(BusinessException):
    pass


class SalesOrderCannotBeReturnedException(BusinessException):
    pass


class SalesOrderValidationException(BusinessException):
    pass


class InsufficientStockException(BusinessException):
    pass
