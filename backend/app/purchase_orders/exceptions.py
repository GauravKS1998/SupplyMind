from app.exceptions.common import (
    NotFoundException,
    AlreadyExistsException,
    BusinessException,
    InternalServerException,
)


class PurchaseOrderAlreadyExistsException(AlreadyExistsException):
    pass


class PurchaseOrderNotFoundException(NotFoundException):
    pass


class PurchaseOrderNotDraftedException(BusinessException):
    pass


class PurchaseOrderNotSubmittedException(BusinessException):
    pass


class PurchaseOrderNotApprovedException(BusinessException):
    pass


class PurchaseOrderNotOrderedException(BusinessException):
    pass


class PurchaseOrderNotInTransitException(BusinessException):
    pass


class PurchaseOrderNotReceivedException(BusinessException):
    pass


class PurchaseOrderCannotBeCancelledException(BusinessException):
    pass


class PurchaseOrderFailException(InternalServerException):
    pass
