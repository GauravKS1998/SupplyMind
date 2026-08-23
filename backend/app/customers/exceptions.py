from app.exceptions.common import (
    AlreadyExistsException,
    BusinessException,
    NotFoundException,
    UnauthorizedException,
)


class CustomerNotFoundException(NotFoundException):
    pass


class CustomerAlreadyExistsException(AlreadyExistsException):
    pass


class CustomerAccessDeniedException(UnauthorizedException):
    pass


class InvalidCustomerStateException(BusinessException):
    pass
