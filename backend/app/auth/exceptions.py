class AuthException(Exception):
    pass


class UserAlreadyExistsException(AuthException):
    pass


class InvalidRoleException(AuthException):
    pass


class InvalidCredentialsException(AuthException):
    pass


class UserNotFoundException(AuthException):
    pass


class AccountPendingApprovalException(AuthException):
    pass
