class AuthException(Exception):
    pass


class InvalidCredentialsException(AuthException):
    pass


class AccountPendingApprovalException(AuthException):
    pass
