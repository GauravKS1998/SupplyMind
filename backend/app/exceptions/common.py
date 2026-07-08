from .base_exception import BaseAPIException


class ValidationException(BaseAPIException):

    def __init__(self, message):
        super().__init__(400, message)


class UnauthorizedException(BaseAPIException):

    def __init__(self, message):
        super().__init__(401, message)


class ForbiddenException(BaseAPIException):

    def __init__(self, message):
        super().__init__(403, message)


class NotFoundException(BaseAPIException):

    def __init__(self, message):
        super().__init__(404, message)


class ConflictException(BaseAPIException):

    def __init__(self, message):
        super().__init__(409, message)


class AlreadyExistsException(ConflictException):

    pass


class BusinessException(BaseAPIException):

    def __init__(self, message):
        super().__init__(422, message)


class InternalServerException(BaseAPIException):

    def __init__(self, message):
        super().__init__(500, message)
