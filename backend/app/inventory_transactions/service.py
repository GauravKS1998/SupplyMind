from math import ceil

from sqlalchemy.orm import Session

from app.common.responses import PaginatedResponse
from app.common.pagination import PaginationMeta

from .model import InventoryTransaction
from .enums import (
    InventoryTransactionType,
    InventoryReferenceType,
)

from app.inventories.model import Inventory

from .schema import InventoryTransactionSearchRequest
from .repository import (
    save,
    find_by_id,
    find_transactions,
)
from .mapper import (
    map_transaction,
    map_transactions,
)
from .validators import validate_transaction_exists


def create_transaction(
    db: Session,
    inventory_id: int,
    transaction_type: InventoryTransactionType,
    quantity_before: int,
    quantity_delta: int,
    quantity_after: int,
    reserved_quantity_before: int,
    reserved_quantity_after: int,
    available_quantity_before: int,
    available_quantity_after: int,
    created_by: int,
    reason: str | None = None,
    reference_type: InventoryReferenceType | None = None,
    reference_id: int | None = None,
):
    transaction = InventoryTransaction(
        inventory_id=inventory_id,
        transaction_type=transaction_type,
        quantity_before=quantity_before,
        quantity_delta=quantity_delta,
        quantity_after=quantity_after,
        reserved_quantity_before=reserved_quantity_before,
        reserved_quantity_after=reserved_quantity_after,
        available_quantity_before=available_quantity_before,
        available_quantity_after=available_quantity_after,
        reason=reason,
        reference_type=reference_type,
        reference_id=reference_id,
        created_by=created_by,
    )

    save(db, transaction)

    return transaction


def get_transaction(
    db: Session,
    transaction_id: int,
):
    transaction = validate_transaction_exists(
        db,
        transaction_id,
    )

    return map_transaction(transaction)


def search_transactions(
    db: Session,
    request: InventoryTransactionSearchRequest,
):
    transactions, total_items = find_transactions(
        db=db,
        page=request.page,
        size=request.size,
        search=request.search,
        inventory_id=request.inventory_id,
        transaction_type=request.transaction_type,
        reference_type=request.reference_type,
        reference_id=request.reference_id,
        created_by=request.created_by,
        sort_by=request.sort_by,
        direction=request.direction,
    )

    total_pages = ceil(total_items / request.size) if total_items > 0 else 0

    return PaginatedResponse(
        items=map_transactions(transactions),
        pagination=PaginationMeta(
            page=request.page,
            size=request.size,
            total_items=total_items,
            total_pages=total_pages,
            has_next=request.page < total_pages,
            has_previous=request.page > 1,
        ),
    )
