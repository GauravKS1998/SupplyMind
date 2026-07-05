class SupplierException(Exception):
    pass


class SupplierNotFoundException(SupplierException):
    pass


class UnauthorizedAccessException(SupplierException):
    pass
