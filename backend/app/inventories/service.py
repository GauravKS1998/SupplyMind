from math import ceil
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.common.responses import PaginatedResponse
from app.common.pagination import PaginationMeta

from app.logging.logger import logger

from .model import Inventory

from .schema import (
    InventoryCreateRequest,
    InventoryUpdateRequest,
    InventorySearchRequest,
    InventoryIncreaseRequest,
    InventoryDecreaseRequest,
    InventoryReserveRequest,
    InventoryReleaseRequest,
    InventoryAdjustRequest,
)

from app.inventory_transactions.service import create_transaction

from app.inventory_transactions.enums import (
    InventoryTransactionType,
    InventoryReferenceType,
)

from .repository import (
    save,
    find_all,
    find_all_active,
    find_all_inactive,
    find_inventories,
)

from .mapper import (
    map_inventory,
    map_inventories,
)

from .validators import (
    validate_inventory_exists,
    validate_inventory_is_active,
    validate_product_exists,
    validate_warehouse_exists,
    validate_duplicate_inventory,
    validate_quantity,
    validate_reserved_quantity,
    validate_reorder_level,
    validate_reorder_quantity,
    validate_unit_cost,
    validate_dates,
    calculate_available_quantity,
    validate_inventory_decrease,
    validate_inventory_reservation,
    validate_inventory_release,
    validate_inventory_adjustment,
)


def get_all_inventories(
    db: Session,
):
    inventories = find_all(db)

    return map_inventories(inventories)


def get_active_inventories(
    db: Session,
):
    inventories = find_all_active(db)

    return map_inventories(inventories)


def get_inactive_inventories(
    db: Session,
):
    inventories = find_all_inactive(db)

    return map_inventories(inventories)


def get_inventory_by_id(
    db: Session,
    inventory_id: int,
):
    inventory = validate_inventory_exists(
        db,
        inventory_id,
    )

    return map_inventory(inventory)


def search_inventories(
    db: Session,
    request: InventorySearchRequest,
):
    inventories, total_items = find_inventories(
        db=db,
        page=request.page,
        size=request.size,
        search=request.search,
        warehouse_id=request.warehouse_id,
        product_id=request.product_id,
        batch_number=request.batch_number,
        is_active=request.is_active,
        expiry_before=request.expiry_before,
        expiry_after=request.expiry_after,
        manufacturing_before=request.manufacturing_before,
        manufacturing_after=request.manufacturing_after,
        low_stock_only=request.low_stock_only,
        sort_by=request.sort_by,
        direction=request.direction,
    )

    total_pages = ceil(total_items / request.size) if total_items > 0 else 0

    return PaginatedResponse(
        items=map_inventories(inventories),
        pagination=PaginationMeta(
            page=request.page,
            size=request.size,
            total_items=total_items,
            total_pages=total_pages,
            has_next=request.page < total_pages,
            has_previous=request.page > 1,
        ),
    )


def create_inventory(
    db: Session,
    request: InventoryCreateRequest,
    current_user_id: int,
):
    # ---------------------------------------------------------
    # Validate Master Data
    # ---------------------------------------------------------

    validate_product_exists(
        db,
        request.product_id,
    )

    validate_warehouse_exists(
        db,
        request.warehouse_id,
    )

    # ---------------------------------------------------------
    # Validate Duplicate Inventory
    # ---------------------------------------------------------

    validate_duplicate_inventory(
        db,
        request.product_id,
        request.warehouse_id,
        request.batch_number,
    )

    # ---------------------------------------------------------
    # Validate Business Rules
    # ---------------------------------------------------------

    validate_quantity(
        request.quantity,
    )

    validate_reorder_level(
        request.reorder_level,
    )

    validate_reorder_quantity(
        request.reorder_quantity,
    )

    validate_unit_cost(
        request.unit_cost,
    )

    validate_dates(
        request.manufacturing_date,
        request.expiry_date,
    )

    # ---------------------------------------------------------
    # Create Inventory
    # ---------------------------------------------------------

    inventory = Inventory(
        product_id=request.product_id,
        warehouse_id=request.warehouse_id,
        quantity=request.quantity,
        reserved_quantity=0,
        available_quantity=calculate_available_quantity(
            request.quantity,
            0,
        ),
        unit_cost=request.unit_cost,
        reorder_level=request.reorder_level,
        reorder_quantity=request.reorder_quantity,
        batch_number=request.batch_number,
        manufacturing_date=request.manufacturing_date,
        expiry_date=request.expiry_date,
        storage_location=request.storage_location,
        created_by=current_user_id,
    )

    save(
        db,
        inventory,
    )

    # ---------------------------------------------------------
    # Flush so inventory.id is available
    # ---------------------------------------------------------

    db.flush()

    # ---------------------------------------------------------
    # Record Initial Inventory Transaction
    # ---------------------------------------------------------

    create_transaction(
        db=db,
        inventory_id=inventory.id,
        transaction_type=InventoryTransactionType.CREATE,
        quantity_before=0,
        quantity_delta=inventory.quantity,
        quantity_after=inventory.quantity,
        reserved_quantity_before=0,
        reserved_quantity_after=inventory.reserved_quantity,
        available_quantity_before=0,
        available_quantity_after=inventory.available_quantity,
        created_by=current_user_id,
        reason="Initial inventory creation",
        reference_type=InventoryReferenceType.INVENTORY,
        reference_id=inventory.id,
    )

    # ---------------------------------------------------------
    # Commit Once
    # ---------------------------------------------------------

    db.commit()

    db.refresh(inventory)

    logger.info(f"Inventory {inventory.id} created successfully.")

    return map_inventory(
        inventory,
    )


def update_inventory(
    db: Session,
    inventory_id: int,
    request: InventoryUpdateRequest,
    current_user_id: int,
):
    inventory = validate_inventory_exists(
        db,
        inventory_id,
    )

    validate_inventory_is_active(
        inventory,
    )

    # -------------------------
    # Validate Business Rules
    # -------------------------

    validate_reorder_level(
        request.reorder_level,
    )

    validate_reorder_quantity(
        request.reorder_quantity,
    )

    validate_unit_cost(
        request.unit_cost,
    )

    validate_dates(
        request.manufacturing_date,
        request.expiry_date,
    )

    # -------------------------
    # Update Metadata
    # -------------------------

    inventory.unit_cost = request.unit_cost

    inventory.reorder_level = request.reorder_level
    inventory.reorder_quantity = request.reorder_quantity

    inventory.manufacturing_date = request.manufacturing_date
    inventory.expiry_date = request.expiry_date

    inventory.storage_location = request.storage_location

    inventory.updated_by = current_user_id
    inventory.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(inventory)

    logger.info(f"Inventory {inventory.id} metadata updated.")

    return map_inventory(inventory)


def deactivate_inventory(
    db: Session,
    inventory_id: int,
    current_user_id: int,
):
    inventory = validate_inventory_exists(
        db,
        inventory_id,
    )

    if not inventory.is_active:
        return {"message": "Inventory already inactive"}

    inventory.is_active = False
    inventory.deactivated_by = current_user_id

    update_inventory_audit(
        inventory,
        current_user_id,
    )

    db.commit()
    db.refresh(inventory)

    logger.info(f"Inventory {inventory.id} deactivated.")

    return {"message": "Inventory deactivated successfully"}


def reactivate_inventory(
    db: Session,
    inventory_id: int,
    current_user_id: int,
):
    inventory = validate_inventory_exists(
        db,
        inventory_id,
    )

    if inventory.is_active:
        return {"message": "Inventory already active"}

    inventory.is_active = True
    inventory.reactivated_by = current_user_id

    update_inventory_audit(
        inventory,
        current_user_id,
    )

    db.commit()
    db.refresh(inventory)

    logger.info(f"Inventory {inventory.id} reactivated.")

    return {"message": "Inventory reactivated successfully"}


def capture_inventory_state(
    inventory: Inventory,
) -> dict:
    """
    Captures the current inventory state for transaction logging.
    """

    return {
        "quantity": inventory.quantity,
        "reserved_quantity": inventory.reserved_quantity,
        "available_quantity": inventory.available_quantity,
    }


def update_inventory_audit(
    inventory: Inventory,
    current_user_id: int,
):
    """
    Updates common audit fields.
    """

    inventory.updated_by = current_user_id
    inventory.updated_at = datetime.now(timezone.utc)


def increase_inventory(
    db: Session,
    inventory_id: int,
    request: InventoryIncreaseRequest,
    current_user_id: int,
):
    inventory = validate_inventory_exists(
        db,
        inventory_id,
    )

    validate_inventory_is_active(
        inventory,
    )

    # ---------------------------------------------------------
    # Capture Before State
    # ---------------------------------------------------------

    before = capture_inventory_state(
        inventory,
    )

    # ---------------------------------------------------------
    # Apply Inventory Increase
    # ---------------------------------------------------------

    inventory.quantity += request.quantity

    inventory.available_quantity = calculate_available_quantity(
        inventory.quantity,
        inventory.reserved_quantity,
    )

    update_inventory_audit(
        inventory,
        current_user_id,
    )

    # ---------------------------------------------------------
    # Capture After State
    # ---------------------------------------------------------

    after = capture_inventory_state(
        inventory,
    )

    # ---------------------------------------------------------
    # Record Transaction
    # ---------------------------------------------------------

    create_transaction(
        db=db,
        inventory_id=inventory.id,
        transaction_type=InventoryTransactionType.INCREASE,
        quantity_before=before["quantity"],
        quantity_delta=request.quantity,
        quantity_after=after["quantity"],
        reserved_quantity_before=before["reserved_quantity"],
        reserved_quantity_after=after["reserved_quantity"],
        available_quantity_before=before["available_quantity"],
        available_quantity_after=after["available_quantity"],
        created_by=current_user_id,
        reason=request.reason,
        reference_type=request.reference_type,
        reference_id=request.reference_id,
    )

    db.commit()

    db.refresh(
        inventory,
    )

    logger.info(f"Inventory {inventory.id} increased by {request.quantity}.")

    return map_inventory(
        inventory,
    )


def decrease_inventory(
    db: Session,
    inventory_id: int,
    request: InventoryDecreaseRequest,
    current_user_id: int,
):
    inventory = validate_inventory_exists(
        db,
        inventory_id,
    )

    validate_inventory_is_active(
        inventory,
    )

    # ---------------------------------------------------------
    # Validate Business Rules
    # ---------------------------------------------------------

    validate_inventory_decrease(
        inventory,
        request.quantity,
    )

    # ---------------------------------------------------------
    # Capture Before State
    # ---------------------------------------------------------

    before = capture_inventory_state(
        inventory,
    )

    # ---------------------------------------------------------
    # Apply Inventory Decrease
    # ---------------------------------------------------------

    inventory.quantity -= request.quantity

    inventory.available_quantity = calculate_available_quantity(
        inventory.quantity,
        inventory.reserved_quantity,
    )

    update_inventory_audit(
        inventory,
        current_user_id,
    )

    # ---------------------------------------------------------
    # Capture After State
    # ---------------------------------------------------------

    after = capture_inventory_state(
        inventory,
    )

    # ---------------------------------------------------------
    # Record Transaction
    # ---------------------------------------------------------

    create_transaction(
        db=db,
        inventory_id=inventory.id,
        transaction_type=InventoryTransactionType.DECREASE,
        quantity_before=before["quantity"],
        quantity_delta=-request.quantity,
        quantity_after=after["quantity"],
        reserved_quantity_before=before["reserved_quantity"],
        reserved_quantity_after=after["reserved_quantity"],
        available_quantity_before=before["available_quantity"],
        available_quantity_after=after["available_quantity"],
        created_by=current_user_id,
        reason=request.reason,
        reference_type=request.reference_type,
        reference_id=request.reference_id,
    )

    db.commit()

    db.refresh(
        inventory,
    )

    logger.info(f"Inventory {inventory.id} decreased by {request.quantity}.")

    return map_inventory(
        inventory,
    )


def reserve_inventory(
    db: Session,
    inventory_id: int,
    request: InventoryReserveRequest,
    current_user_id: int,
):
    inventory = validate_inventory_exists(
        db,
        inventory_id,
    )

    validate_inventory_is_active(
        inventory,
    )

    validate_inventory_reservation(
        inventory,
        request.quantity,
    )

    before = capture_inventory_state(
        inventory,
    )

    # ---------------------------------------------------------
    # Apply Reservation
    # ---------------------------------------------------------

    inventory.reserved_quantity += request.quantity

    inventory.available_quantity = calculate_available_quantity(
        inventory.quantity,
        inventory.reserved_quantity,
    )

    update_inventory_audit(
        inventory,
        current_user_id,
    )

    after = capture_inventory_state(
        inventory,
    )

    create_transaction(
        db=db,
        inventory_id=inventory.id,
        transaction_type=InventoryTransactionType.RESERVE,
        quantity_before=before["quantity"],
        quantity_delta=0,
        quantity_after=after["quantity"],
        reserved_quantity_before=before["reserved_quantity"],
        reserved_quantity_after=after["reserved_quantity"],
        available_quantity_before=before["available_quantity"],
        available_quantity_after=after["available_quantity"],
        created_by=current_user_id,
        reason=request.reason,
        reference_type=request.reference_type,
        reference_id=request.reference_id,
    )

    db.commit()

    db.refresh(
        inventory,
    )

    logger.info(f"Reserved {request.quantity} units for inventory {inventory.id}.")

    return map_inventory(
        inventory,
    )


def release_inventory(
    db: Session,
    inventory_id: int,
    request: InventoryReleaseRequest,
    current_user_id: int,
):
    inventory = validate_inventory_exists(
        db,
        inventory_id,
    )

    validate_inventory_is_active(
        inventory,
    )

    # ---------------------------------------------------------
    # Validate Business Rules
    # ---------------------------------------------------------

    validate_inventory_release(
        inventory,
        request.quantity,
    )

    # ---------------------------------------------------------
    # Capture Before State
    # ---------------------------------------------------------

    before = capture_inventory_state(
        inventory,
    )

    # ---------------------------------------------------------
    # Release Inventory
    # ---------------------------------------------------------

    inventory.reserved_quantity -= request.quantity

    inventory.available_quantity = calculate_available_quantity(
        inventory.quantity,
        inventory.reserved_quantity,
    )

    update_inventory_audit(
        inventory,
        current_user_id,
    )

    # ---------------------------------------------------------
    # Capture After State
    # ---------------------------------------------------------

    after = capture_inventory_state(
        inventory,
    )

    # ---------------------------------------------------------
    # Record Transaction
    # ---------------------------------------------------------

    create_transaction(
        db=db,
        inventory_id=inventory.id,
        transaction_type=InventoryTransactionType.RELEASE,
        quantity_before=before["quantity"],
        quantity_delta=0,
        quantity_after=after["quantity"],
        reserved_quantity_before=before["reserved_quantity"],
        reserved_quantity_after=after["reserved_quantity"],
        available_quantity_before=before["available_quantity"],
        available_quantity_after=after["available_quantity"],
        created_by=current_user_id,
        reason=request.reason,
        reference_type=request.reference_type,
        reference_id=request.reference_id,
    )

    db.commit()

    db.refresh(
        inventory,
    )

    logger.info(
        f"Released {request.quantity} reserved units for inventory {inventory.id}."
    )

    return map_inventory(
        inventory,
    )


def adjust_inventory(
    db: Session,
    inventory_id: int,
    request: InventoryAdjustRequest,
    current_user_id: int,
):
    inventory = validate_inventory_exists(
        db,
        inventory_id,
    )

    validate_inventory_is_active(
        inventory,
    )

    validate_inventory_adjustment(
        inventory,
        request.quantity,
    )

    before = capture_inventory_state(
        inventory,
    )

    # ---------------------------------------------------------
    # Calculate Delta
    # ---------------------------------------------------------

    quantity_delta = request.quantity - inventory.quantity

    # ---------------------------------------------------------
    # Apply Adjustment
    # ---------------------------------------------------------

    inventory.quantity = request.quantity

    inventory.available_quantity = calculate_available_quantity(
        inventory.quantity,
        inventory.reserved_quantity,
    )

    update_inventory_audit(
        inventory,
        current_user_id,
    )

    after = capture_inventory_state(
        inventory,
    )

    create_transaction(
        db=db,
        inventory_id=inventory.id,
        transaction_type=InventoryTransactionType.ADJUSTMENT,
        quantity_before=before["quantity"],
        quantity_delta=quantity_delta,
        quantity_after=after["quantity"],
        reserved_quantity_before=before["reserved_quantity"],
        reserved_quantity_after=after["reserved_quantity"],
        available_quantity_before=before["available_quantity"],
        available_quantity_after=after["available_quantity"],
        created_by=current_user_id,
        reason=request.reason,
        reference_type=request.reference_type,
        reference_id=request.reference_id,
    )

    db.commit()

    db.refresh(
        inventory,
    )

    logger.info(
        f"Inventory {inventory.id} adjusted from "
        f"{before['quantity']} to {after['quantity']}."
    )

    return map_inventory(
        inventory,
    )
