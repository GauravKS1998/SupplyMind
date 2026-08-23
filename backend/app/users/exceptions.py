from app.exceptions.common import (
    AlreadyExistsException,
    BusinessException,
    NotFoundException,
)


class UserAlreadyExistsException(AlreadyExistsException):
    pass


class InvalidUserStateException(BusinessException):
    pass


class InvalidRoleException(BusinessException):
    pass


class UserNotFoundException(NotFoundException):
    pass
