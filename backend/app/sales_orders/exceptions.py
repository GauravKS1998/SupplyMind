class SalesOrderException(Exception):
    pass


class SalesOrderAlreadyExistsException(SalesOrderException):
    pass


class SalesOrderNotFoundException(SalesOrderException):
    pass


class SalesOrderNotDraftedException(SalesOrderException):
    pass


class SalesOrderNotConfirmedException(SalesOrderException):
    pass


class SalesOrderNotReservedException(SalesOrderException):
    pass


class SalesOrderNotDispatchedException(SalesOrderException):
    pass


class SalesOrderNotDeliveredException(SalesOrderException):
    pass


class SalesOrderCannotBeCancelledException(SalesOrderException):
    pass


class ProductNotFoundException(SalesOrderException):
    pass


class InventoryNotFoundException(SalesOrderException):
    pass


class InsufficientStockException(SalesOrderException):
    pass


class SalesOrderFailException(SalesOrderException):
    pass
