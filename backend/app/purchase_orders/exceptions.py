from app.exceptions.common import (
    BusinessException,
    NotFoundException,
)


class PurchaseOrderNotFoundException(NotFoundException):
    pass


class PurchaseOrderCannotBeModifiedException(BusinessException):
    pass


class PurchaseOrderCannotBeSubmittedException(BusinessException):
    pass


class PurchaseOrderCannotBeApprovedException(BusinessException):
    pass


class PurchaseOrderCannotBeRejectedException(BusinessException):
    pass


class PurchaseOrderCannotBeCancelledException(BusinessException):
    pass


class PurchaseOrderCannotBeClosedException(BusinessException):
    pass


class PurchaseOrderValidationException(BusinessException):
    pass


class PurchaseOrderLineNotFoundException(NotFoundException):

    def __init__(self, purchase_order_line_id: int):
        super().__init__(
            f"Purchase Order Line with id '{purchase_order_line_id}' was not found."
        )
