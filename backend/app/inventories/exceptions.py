class InventoryException(Exception):
    pass


class InventoryNotFoundException(InventoryException):
    pass


class InventoryAlreadyExistsException(InventoryException):
    pass
