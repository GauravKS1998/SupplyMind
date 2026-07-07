class PurchaseOrderException(Exception):
    pass


class PurchaseOrderAlreadyExistsException(PurchaseOrderException):
    pass


class PurchaseOrderNotFoundException(PurchaseOrderException):
    pass


class PurchaseOrderNotDraftedException(PurchaseOrderException):
    pass


class PurchaseOrderNotSubmittedException(PurchaseOrderException):
    pass


class PurchaseOrderNotApprovedException(PurchaseOrderException):
    pass


class PurchaseOrderNotOrderedException(PurchaseOrderException):
    pass


class PurchaseOrderNotInTransitException(PurchaseOrderException):
    pass


class PurchaseOrderNotReceivedException(PurchaseOrderException):
    pass


class PurchaseOrderCannotBeCancelledException(PurchaseOrderException):
    pass


class PurchaseOrderFailException(PurchaseOrderException):
    pass
