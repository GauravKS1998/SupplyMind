from datetime import date

from sqlalchemy.orm import Session

from app.common.entity_utils import get_or_raise

from app.products.repository import find_by_id as find_product_by_id
from app.warehouses.repository import find_by_id as find_warehouse_by_id

from .model import Inventory

from .repository import (
    find_by_id,
    find_duplicate_inventory,
)

from .exceptions import (
    InventoryNotFoundException,
    InventoryInactiveException,
    InventoryAlreadyExistsException,
    InvalidInventoryQuantityException,
    InvalidReservedQuantityException,
    InvalidReorderLevelException,
    InvalidUnitCostException,
    InvalidInventoryDatesException,
)


def validate_inventory_exists(
    db: Session,
    inventory_id: int,
):
    """
    Ensures inventory exists.
    """

    return get_or_raise(
        find_by_id(db, inventory_id),
        InventoryNotFoundException("Inventory not found"),
    )


def validate_inventory_is_active(
    inventory: Inventory,
):
    if not inventory.is_active:
        raise InventoryInactiveException("Inventory is inactive.")


def validate_product_exists(
    db: Session,
    product_id: int,
):
    """
    Ensures product exists.
    """

    return get_or_raise(
        find_product_by_id(db, product_id),
        InventoryNotFoundException("Product not found"),
    )


def validate_warehouse_exists(
    db: Session,
    warehouse_id: int,
):
    """
    Ensures warehouse exists.
    """

    return get_or_raise(
        find_warehouse_by_id(db, warehouse_id),
        InventoryNotFoundException("Warehouse not found"),
    )


def validate_duplicate_inventory(
    db: Session,
    product_id: int,
    warehouse_id: int,
    batch_number: str,
):
    """
    Prevent duplicate inventory
    for same Product + Warehouse + Batch.
    """

    existing = find_duplicate_inventory(
        db,
        product_id,
        warehouse_id,
        batch_number,
    )

    if existing:
        raise InventoryAlreadyExistsException(
            "Inventory already exists for this Product, Warehouse and Batch."
        )


def validate_quantity(quantity: int):
    """
    Quantity cannot be negative.
    """

    if quantity < 0:
        raise InvalidInventoryQuantityException("Quantity cannot be negative.")


def validate_reserved_quantity(
    inventory: Inventory,
):
    """
    Validates reserved quantity constraints.
    """

    if inventory.reserved_quantity < 0:
        raise InvalidReservedQuantityException("Reserved quantity cannot be negative.")

    if inventory.reserved_quantity > inventory.quantity:
        raise InvalidReservedQuantityException(
            "Reserved quantity cannot exceed total quantity."
        )


def validate_reorder_level(
    reorder_level: int,
):
    if reorder_level < 0:
        raise InvalidReorderLevelException("Reorder level cannot be negative.")


def validate_reorder_quantity(
    reorder_quantity: int,
):
    if reorder_quantity < 0:
        raise InvalidReorderLevelException("Reorder quantity cannot be negative.")


def validate_unit_cost(
    unit_cost: float,
):
    if unit_cost < 0:
        raise InvalidUnitCostException("Unit cost cannot be negative.")


def validate_dates(
    manufacturing_date: date | None,
    expiry_date: date | None,
):
    """
    Manufacturing date
    cannot be after expiry date.
    """

    if manufacturing_date and expiry_date and manufacturing_date > expiry_date:
        raise InvalidInventoryDatesException(
            "Manufacturing date cannot be after expiry date."
        )


def calculate_available_quantity(
    quantity: int,
    reserved_quantity: int,
):
    """
    Returns available quantity.
    """

    return quantity - reserved_quantity


def validate_inventory_decrease(
    inventory: Inventory,
    quantity_to_decrease: int,
):
    """
    Validates that the inventory has enough available stock
    to decrease the requested quantity.
    """

    if quantity_to_decrease <= 0:
        raise InvalidInventoryQuantityException(
            "Quantity to decrease must be greater than zero."
        )

    if quantity_to_decrease > inventory.available_quantity:
        raise InvalidInventoryQuantityException("Insufficient available inventory.")


def validate_inventory_reservation(
    inventory: Inventory,
    quantity_to_reserve: int,
):
    """
    Validates that sufficient available inventory exists
    for reservation.
    """

    if quantity_to_reserve <= 0:
        raise InvalidReservedQuantityException(
            "Reservation quantity must be greater than zero."
        )

    if quantity_to_reserve > inventory.available_quantity:
        raise InvalidReservedQuantityException(
            "Insufficient available inventory for reservation."
        )


def validate_inventory_release(
    inventory: Inventory,
    quantity_to_release: int,
):
    """
    Validates that sufficient inventory is reserved
    to release the requested quantity.
    """

    if quantity_to_release <= 0:
        raise InvalidInventoryQuantityException(
            "Release quantity must be greater than zero."
        )

    if quantity_to_release > inventory.reserved_quantity:
        raise InvalidReservedQuantityException(
            "Cannot release more than the reserved quantity."
        )


def validate_inventory_adjustment(
    inventory: Inventory,
    adjusted_quantity: int,
):
    """
    Validates an inventory adjustment request.
    """

    if adjusted_quantity < 0:
        raise InvalidInventoryQuantityException("Adjusted quantity cannot be negative.")

    if adjusted_quantity < inventory.reserved_quantity:
        raise InvalidReservedQuantityException(
            "Adjusted quantity cannot be less than reserved quantity."
        )
