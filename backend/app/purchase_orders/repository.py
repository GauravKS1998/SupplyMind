from sqlalchemy import func, select
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.common.search import apply_search
from app.common.filtering import apply_filter
from app.common.sorting import apply_sorting

from .model import (
    PurchaseOrder,
    PurchaseOrderLine,
)

from app.products.model import Product

ALLOWED_SORT_FIELDS = {
    "po_number": PurchaseOrder.po_number,
    "status": PurchaseOrder.status,
    "created_at": PurchaseOrder.created_at,
    "expected_delivery_date": PurchaseOrder.expected_delivery_date,
    "grand_total": PurchaseOrder.grand_total,
}


def save_purchase_order(
    db: Session,
    purchase_order: PurchaseOrder,
) -> PurchaseOrder:

    db.add(purchase_order)
    db.flush()

    return purchase_order


def delete_purchase_order_lines(
    db: Session,
    purchase_order_id: int,
):

    db.query(PurchaseOrderLine).filter(
        PurchaseOrderLine.purchase_order_id == purchase_order_id
    ).delete(synchronize_session=False)


def find_purchase_order_by_id(
    db: Session,
    purchase_order_id: int,
):

    return (
        db.query(PurchaseOrder)
        .options(
            joinedload(PurchaseOrder.lines)
            .joinedload(PurchaseOrderLine.product)
            .joinedload(Product.uom),
            joinedload(PurchaseOrder.supplier),
            joinedload(PurchaseOrder.warehouse),
        )
        .filter(PurchaseOrder.id == purchase_order_id)
        .first()
    )


def find_purchase_order_by_number(
    db: Session,
    po_number: str,
):

    return db.query(PurchaseOrder).filter(PurchaseOrder.po_number == po_number).first()


def search_purchase_orders(
    db: Session,
    request,
):
    query = db.query(PurchaseOrder).options(
        joinedload(PurchaseOrder.supplier),
        joinedload(PurchaseOrder.warehouse),
    )

    # =========================
    # Filter
    # =========================

    query = apply_filter(
        query,
        PurchaseOrder.supplier_id,
        request.supplier_id,
    )

    query = apply_filter(
        query,
        PurchaseOrder.warehouse_id,
        request.warehouse_id,
    )

    query = apply_filter(
        query,
        PurchaseOrder.status,
        request.status,
    )

    # =========================
    # Search
    # =========================

    query = apply_search(
        query,
        PurchaseOrder.po_number,
        request.po_number,
    )

    if request.expected_delivery_from:
        query = query.filter(
            PurchaseOrder.expected_delivery_date >= request.expected_delivery_from
        )

    if request.expected_delivery_to:
        query = query.filter(
            PurchaseOrder.expected_delivery_date <= request.expected_delivery_to
        )

    # =========================
    # Sorting
    # =========================

    total_records = query.with_entities(func.count(PurchaseOrder.id)).scalar()

    query = apply_sorting(
        query,
        request.sort_by,
        request.sort_direction,
        ALLOWED_SORT_FIELDS,
    )

    results = query.offset(request.offset).limit(request.page_size).all()

    return results, total_records
