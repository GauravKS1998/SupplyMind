from app.exceptions.common import (
    NotFoundException,
    AlreadyExistsException,
    InternalServerException,
)


class CustomerNotFoundException(NotFoundException):
    pass


class CustomerAlreadyExistsException(AlreadyExistsException):
    pass


class CustomerFailException(InternalServerException):
    pass
