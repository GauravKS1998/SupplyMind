class WarehouseException(Exception):
    pass


class WarehouseAlreadyExistsException(WarehouseException):
    pass


class WarehouseNotFoundException(WarehouseException):
    pass
