from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.common.filtering import apply_filter
from app.common.search import apply_search
from app.common.sorting import apply_sorting

from app.products.model import Product

from .model import (
    SalesOrder,
    SalesOrderLine,
)

ALLOWED_SORT_FIELDS = {
    "so_number": SalesOrder.so_number,
    "status": SalesOrder.status,
    "created_at": SalesOrder.created_at,
    "grand_total": SalesOrder.grand_total,
}


def sales_order_query(
    db: Session,
):
    return db.query(SalesOrder).options(
        joinedload(SalesOrder.lines)
        .joinedload(SalesOrderLine.product)
        .joinedload(Product.uom),
        joinedload(SalesOrder.warehouse),
        joinedload(SalesOrder.customer),
    )


def save_sales_order(
    db: Session,
    sales_order: SalesOrder,
) -> SalesOrder:

    db.add(sales_order)
    db.flush()

    return sales_order


def find_sales_order_by_id(
    db: Session,
    sales_order_id: int,
):
    return (
        sales_order_query(db)
        .filter(
            SalesOrder.id == sales_order_id,
        )
        .first()
    )


def find_sales_order_by_number(
    db: Session,
    so_number: str,
):

    return (
        db.query(SalesOrder)
        .filter(
            SalesOrder.so_number == so_number,
        )
        .first()
    )


def search_sales_orders(
    db: Session,
    request,
):

    query = sales_order_query(db)

    # =========================
    # Filter
    # =========================

    query = apply_filter(
        query,
        SalesOrder.customer_id,
        request.customer_id,
    )

    query = apply_filter(
        query,
        SalesOrder.warehouse_id,
        request.warehouse_id,
    )

    query = apply_filter(
        query,
        SalesOrder.status,
        request.status,
    )

    # =========================
    # Search
    # =========================

    query = apply_search(
        query,
        SalesOrder.so_number,
        request.so_number,
    )

    # =========================
    # Date Filter
    # =========================

    if request.created_from:
        query = query.filter(
            SalesOrder.created_at >= request.created_from,
        )

    if request.created_to:
        query = query.filter(
            SalesOrder.created_at <= request.created_to,
        )

    # =========================
    # Count
    # =========================

    total_items = query.with_entities(func.count(SalesOrder.id)).scalar()

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
