from sqlalchemy.orm import Session

from app.common.filtering import apply_filter
from app.common.search import apply_search
from app.common.sorting import apply_sorting

from .model import InventoryTransaction


def save(
    db: Session,
    transaction: InventoryTransaction,
):
    db.add(transaction)
    db.flush()


def find_by_id(
    db: Session,
    transaction_id: int,
):
    return (
        db.query(InventoryTransaction)
        .filter(InventoryTransaction.id == transaction_id)
        .first()
    )


def find_transactions(
    db: Session,
    page: int,
    size: int,
    search: str | None = None,
    inventory_id: int | None = None,
    transaction_type: str | None = None,
    reference_type: str | None = None,
    reference_id: int | None = None,
    created_by: int | None = None,
    sort_by: str = "created_at",
    direction: str = "desc",
):

    query = db.query(InventoryTransaction)

    query = apply_filter(
        query,
        InventoryTransaction,
        inventory_id=inventory_id,
        transaction_type=transaction_type,
        reference_type=reference_type,
        reference_id=reference_id,
        created_by=created_by,
    )

    query = apply_search(
        query,
        search,
        InventoryTransaction.reason,
    )

    query = apply_sorting(
        query,
        InventoryTransaction,
        sort_by,
        direction,
    )

    total_items = query.count()

    items = query.offset((page - 1) * size).limit(size).all()

    return items, total_items
