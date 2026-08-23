from app.exceptions.common import (
    ForbiddenException,
    UnauthorizedException,
)


class InvalidCredentialsException(UnauthorizedException):
    pass


class AccountPendingApprovalException(ForbiddenException):
    pass


class AccountNotApprovedException(ForbiddenException):
    pass


class AccountInactiveException(ForbiddenException):
    pass


class InvalidSignupRoleException(ForbiddenException):
    pass
