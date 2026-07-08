from app.exceptions.common import NotFoundException, ForbiddenException


class SupplierNotFoundException(NotFoundException):
    pass


class AccessDeniedException(ForbiddenException):
    pass
