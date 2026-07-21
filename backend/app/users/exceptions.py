from app.exceptions.common import (
    AlreadyExistsException,
    BusinessException,
    NotFoundException,
    UnauthorizedException,
)


class UserAlreadyExistsException(AlreadyExistsException):
    pass


class InvalidUserStateException(BusinessException):
    pass


class InvalidRoleException(BusinessException):
    pass


class InvalidCredentialsException(UnauthorizedException):
    pass


class UserNotFoundException(NotFoundException):
    pass
