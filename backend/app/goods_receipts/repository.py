from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.common.filtering import apply_filter
from app.common.search import apply_search
from app.common.sorting import apply_sorting

from app.products.model import Product

from .model import (
    GoodsReceipt,
    GoodsReceiptLine,
)

ALLOWED_SORT_FIELDS = {
    "grn_number": GoodsReceipt.grn_number,
    "status": GoodsReceipt.status,
    "created_at": GoodsReceipt.created_at,
}


def save_goods_receipt(
    db: Session,
    goods_receipt: GoodsReceipt,
) -> GoodsReceipt:

    db.add(goods_receipt)
    db.flush()

    return goods_receipt


def find_goods_receipt_by_id(
    db: Session,
    goods_receipt_id: int,
):

    return (
        db.query(GoodsReceipt)
        .options(
            joinedload(GoodsReceipt.lines)
            .joinedload(GoodsReceiptLine.product)
            .joinedload(Product.uom),
            joinedload(GoodsReceipt.purchase_order),
            joinedload(GoodsReceipt.warehouse),
        )
        .filter(GoodsReceipt.id == goods_receipt_id)
        .first()
    )


def find_goods_receipt_by_number(
    db: Session,
    grn_number: str,
):

    return db.query(GoodsReceipt).filter(GoodsReceipt.grn_number == grn_number).first()


def search_goods_receipts(
    db: Session,
    request,
):

    query = db.query(GoodsReceipt).options(
        joinedload(GoodsReceipt.purchase_order),
        joinedload(GoodsReceipt.warehouse),
    )

    # =========================
    # Filter
    # =========================

    query = apply_filter(
        query,
        GoodsReceipt.purchase_order_id,
        request.purchase_order_id,
    )

    query = apply_filter(
        query,
        GoodsReceipt.warehouse_id,
        request.warehouse_id,
    )

    query = apply_filter(
        query,
        GoodsReceipt.status,
        request.status,
    )

    # =========================
    # Search
    # =========================

    query = apply_search(
        query,
        GoodsReceipt.grn_number,
        request.grn_number,
    )

    if request.from_date:
        query = query.filter(GoodsReceipt.created_at >= request.from_date)

    if request.to_date:
        query = query.filter(GoodsReceipt.created_at <= request.to_date)

    # =========================
    # Sorting
    # =========================

    total_records = query.with_entities(func.count(GoodsReceipt.id)).scalar()

    query = apply_sorting(
        query,
        request.sort_by,
        request.sort_direction,
        ALLOWED_SORT_FIELDS,
    )

    results = query.offset(request.offset).limit(request.page_size).all()

    return results, total_records
