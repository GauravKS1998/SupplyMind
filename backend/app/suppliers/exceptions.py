from app.exceptions.common import (
    NotFoundException,
    AlreadyExistsException,
    UnauthorizedException,
)


class SupplierNotFoundException(NotFoundException):
    pass


class SupplierAlreadyExistsException(AlreadyExistsException):
    pass


class SupplierAccessDeniedException(UnauthorizedException):
    pass
