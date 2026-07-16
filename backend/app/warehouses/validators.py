from app.common.entity_utils import get_or_raise

from .repository import find_by_id
from .exceptions import (
    WarehouseNotFoundException,
    InvalidWarehouseCapacityException,
    WarehouseCapacityExceededException,
)


def validate_warehouse_exists(db, warehouse_id: int):
    """
    Ensures warehouse exists.
    Returns warehouse if found.
    """

    return get_or_raise(
        find_by_id(db, warehouse_id),
        WarehouseNotFoundException("Warehouse not found"),
    )


def validate_warehouse_active(warehouse):
    """
    Ensures warehouse is active.
    """

    if not warehouse.is_active:
        raise WarehouseNotFoundException("Warehouse is inactive")

    return warehouse


def validate_capacity(capacity: float):
    """
    Warehouse capacity cannot be zero or negative.
    """

    if capacity <= 0:
        raise InvalidWarehouseCapacityException(
            "Warehouse capacity must be greater than zero"
        )


def validate_utilization(current_utilization: float, capacity: float):
    """
    Utilization cannot exceed capacity.
    """

    if current_utilization < 0:
        raise InvalidWarehouseCapacityException(
            "Current utilization cannot be negative"
        )

    if current_utilization > capacity:
        raise WarehouseCapacityExceededException(
            "Current utilization cannot exceed warehouse capacity"
        )
