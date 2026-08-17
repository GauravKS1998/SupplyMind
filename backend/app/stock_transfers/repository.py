from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.common.filtering import apply_filter
from app.common.search import apply_search
from app.common.sorting import apply_sorting

from app.products.model import Product

from .model import (
    StockTransfer,
    StockTransferLine,
)

ALLOWED_SORT_FIELDS = {
    "transfer_number": StockTransfer.transfer_number,
    "status": StockTransfer.status,
    "created_at": StockTransfer.created_at,
}


def stock_transfer_query(
    db: Session,
):
    return db.query(StockTransfer).options(
        joinedload(StockTransfer.lines)
        .joinedload(StockTransferLine.product)
        .joinedload(Product.uom),
        joinedload(StockTransfer.source_warehouse),
        joinedload(StockTransfer.destination_warehouse),
    )


def save_stock_transfer(
    db: Session,
    stock_transfer: StockTransfer,
) -> StockTransfer:

    db.add(stock_transfer)
    db.flush()

    return stock_transfer


def find_stock_transfer_by_id(
    db: Session,
    stock_transfer_id: int,
):
    return (
        stock_transfer_query(db)
        .filter(
            StockTransfer.id == stock_transfer_id,
        )
        .first()
    )


def find_stock_transfer_by_number(
    db: Session,
    transfer_number: str,
):

    return (
        db.query(StockTransfer)
        .filter(
            StockTransfer.transfer_number == transfer_number,
        )
        .first()
    )


def search_stock_transfers(
    db: Session,
    request,
):

    query = stock_transfer_query(db)

    # =========================
    # Filter
    # =========================

    query = apply_filter(
        query,
        StockTransfer.source_warehouse_id,
        request.source_warehouse_id,
    )

    query = apply_filter(
        query,
        StockTransfer.destination_warehouse_id,
        request.destination_warehouse_id,
    )

    query = apply_filter(
        query,
        StockTransfer.status,
        request.status,
    )

    # =========================
    # Search
    # =========================

    query = apply_search(
        query,
        StockTransfer.transfer_number,
        request.transfer_number,
    )

    # =========================
    # Date Filter
    # =========================

    if request.created_from:
        query = query.filter(
            StockTransfer.created_at >= request.created_from,
        )

    if request.created_to:
        query = query.filter(
            StockTransfer.created_at <= request.created_to,
        )

    # =========================
    # Count
    # =========================

    total_items = query.with_entities(func.count(StockTransfer.id)).scalar()

    # =========================
    # Sorting
    # =========================

    query = apply_sorting(
        query,
        request.sort_by,
        request.sort_direction,
        ALLOWED_SORT_FIELDS,
    )

    # =========================
    # Pagination
    # =========================

    results = query.offset(request.offset).limit(request.page_size).all()

    return results, total_items
