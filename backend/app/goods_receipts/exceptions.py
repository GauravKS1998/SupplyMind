from app.exceptions.common import (
    BusinessException,
    NotFoundException,
)


class GoodsReceiptNotFoundException(NotFoundException):
    pass


class GoodsReceiptLineNotFoundException(NotFoundException):

    def __init__(self, goods_receipt_line_id: int):
        super().__init__(
            f"Goods Receipt Line with id '{goods_receipt_line_id}' was not found."
        )


class PurchaseOrderNotEligibleForReceivingException(BusinessException):
    pass


class DuplicateProductException(BusinessException):
    pass


class ReceivedQuantityExceededException(BusinessException):
    pass


class InvalidAcceptedQuantityException(BusinessException):
    pass


class InvalidRejectedQuantityException(BusinessException):
    pass


class GoodsReceiptHasNoLinesException(BusinessException):
    pass


class GoodsReceiptCannotBeModifiedException(BusinessException):
    pass


class GoodsReceiptCannotBeSubmittedException(BusinessException):
    pass


class GoodsReceiptCannotBeApprovedException(BusinessException):
    pass


class GoodsReceiptCannotBeCancelledException(BusinessException):
    pass


class GoodsReceiptValidationException(BusinessException):
    pass
