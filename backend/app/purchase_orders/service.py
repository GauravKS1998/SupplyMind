from __future__ import annotations

from math import ceil

from decimal import Decimal

from sqlalchemy.orm import Session

from app.common.responses import PaginatedResponse
from app.common.pagination import PaginationMeta

from app.common.entity_utils import get_or_raise

from app.products.model import Product
from app.purchase_orders.enums import PurchaseOrderStatus
from app.purchase_orders.mapper import map_purchase_order, map_purchase_orders
from app.purchase_orders.model import (
    PurchaseOrder,
    PurchaseOrderLine,
)
from app.purchase_orders.repository import (
    find_purchase_order_by_id,
    save_purchase_order,
)
from app.purchase_orders.validators import (
    validate_discount,
    validate_duplicate_products,
    validate_expected_delivery_date,
    validate_ordered_quantity,
    validate_product_exists,
    validate_purchase_order_lines,
    validate_supplier_exists,
    validate_tax,
    validate_unit_price,
    validate_warehouse_exists,
    validate_draft_purchase_order,
    validate_submit_purchase_order,
    validate_approve_purchase_order,
    validate_reject_purchase_order,
    validate_cancel_purchase_order,
    validate_close_purchase_order,
)
from .exceptions import (
    PurchaseOrderNotFoundException,
    PurchaseOrderLineNotFoundException,
)

from .schema import (
    PurchaseOrderCreateRequest,
    PurchaseOrderResponse,
    PurchaseOrderLineCreateRequest,
    PurchaseOrderLineUpdateRequest,
    PurchaseOrderUpdateRequest,
    PurchaseOrderSearchRequest,
)

from app.logging.logger import logger

from app.common.document_number.enums import DocumentType
from app.common.document_number.service import get_next_document_number


def _calculate_purchase_order_totals(
    purchase_order: PurchaseOrder,
):
    subtotal = Decimal("0.00")
    discount_total = Decimal("0.00")
    tax_total = Decimal("0.00")

    for line in purchase_order.lines:

        line.line_total = (
            (line.unit_price * line.ordered_quantity)
            - line.discount_amount
            + line.tax_amount
        )

        subtotal += line.unit_price * line.ordered_quantity
        discount_total += line.discount_amount
        tax_total += line.tax_amount

    purchase_order.subtotal = subtotal
    purchase_order.discount_total = discount_total
    purchase_order.tax_total = tax_total
    purchase_order.grand_total = subtotal - discount_total + tax_total


def _build_purchase_order_lines(
    db: Session,
    request_lines: list[PurchaseOrderLineCreateRequest],
) -> list[PurchaseOrderLine]:

    purchase_order_lines = []

    for request_line in request_lines:

        purchase_order_lines.append(
            _create_purchase_order_line(
                db,
                request_line,
            )
        )

    _renumber_purchase_order_lines(
        purchase_order_lines,
    )

    return purchase_order_lines


def _create_purchase_order_line(
    db: Session,
    request_line: PurchaseOrderLineCreateRequest | PurchaseOrderLineUpdateRequest,
) -> PurchaseOrderLine:

    product: Product = validate_product_exists(
        db,
        request_line.product_id,
    )

    validate_ordered_quantity(request_line.ordered_quantity)

    validate_unit_price(request_line.unit_price)

    validate_discount(request_line.discount_amount)

    validate_tax(request_line.tax_amount)

    return PurchaseOrderLine(
        product_id=product.id,
        product_name_snapshot=product.name,
        product_sku_snapshot=product.sku,
        ordered_quantity=request_line.ordered_quantity,
        received_quantity=0,
        unit_price=request_line.unit_price,
        discount_amount=request_line.discount_amount,
        tax_amount=request_line.tax_amount,
        line_total=Decimal("0.00"),
        remarks=request_line.remarks,
    )


def _update_purchase_order_line(
    db: Session,
    purchase_order_line: PurchaseOrderLine,
    request_line: PurchaseOrderLineUpdateRequest,
):

    product: Product = validate_product_exists(
        db,
        request_line.product_id,
    )

    validate_ordered_quantity(request_line.ordered_quantity)

    validate_unit_price(request_line.unit_price)

    validate_discount(request_line.discount_amount)

    validate_tax(request_line.tax_amount)

    purchase_order_line.product_id = product.id
    purchase_order_line.product_name_snapshot = product.name
    purchase_order_line.product_sku_snapshot = product.sku

    purchase_order_line.ordered_quantity = request_line.ordered_quantity

    purchase_order_line.unit_price = request_line.unit_price

    purchase_order_line.discount_amount = request_line.discount_amount

    purchase_order_line.tax_amount = request_line.tax_amount

    purchase_order_line.remarks = request_line.remarks


def _delete_purchase_order_lines(
    purchase_order: PurchaseOrder,
    deleted_line_ids: list[int],
):

    for deleted_line_id in deleted_line_ids:

        purchase_order_line = get_or_raise(
            _find_purchase_order_line(
                purchase_order,
                deleted_line_id,
            ),
            PurchaseOrderLineNotFoundException(
                deleted_line_id,
            ),
        )

        purchase_order.lines.remove(
            purchase_order_line,
        )


def _renumber_purchase_order_lines(
    purchase_order_lines: list[PurchaseOrderLine],
):

    for index, line in enumerate(
        purchase_order_lines,
        start=1,
    ):
        line.line_number = index


def _populate_purchase_order_header(
    purchase_order: PurchaseOrder,
    request: PurchaseOrderCreateRequest | PurchaseOrderUpdateRequest,
):
    purchase_order.supplier_id = request.supplier_id
    purchase_order.warehouse_id = request.warehouse_id
    purchase_order.expected_delivery_date = request.expected_delivery_date
    purchase_order.remarks = request.remarks


def _find_purchase_order_line(
    purchase_order: PurchaseOrder,
    purchase_order_line_id: int,
) -> PurchaseOrderLine | None:

    return next(
        (line for line in purchase_order.lines if line.id == purchase_order_line_id),
        None,
    )


def _get_purchase_order(
    db: Session,
    purchase_order_id: int,
) -> PurchaseOrder:

    return get_or_raise(
        find_purchase_order_by_id(
            db,
            purchase_order_id,
        ),
        PurchaseOrderNotFoundException(
            purchase_order_id,
        ),
    )


def create_purchase_order(
    db: Session,
    request: PurchaseOrderCreateRequest,
    created_by: int,
) -> PurchaseOrderResponse:

    logger.info(
        "Creating purchase order for supplier_id=%s",
        request.supplier_id,
    )

    validate_supplier_exists(
        db,
        request.supplier_id,
    )

    validate_warehouse_exists(
        db,
        request.warehouse_id,
    )

    validate_purchase_order_lines(request.lines)

    validate_duplicate_products(request.lines)

    validate_expected_delivery_date(request.expected_delivery_date)

    po_number = get_next_document_number(
        db=db,
        document_type=DocumentType.PURCHASE_ORDER,
    )

    purchase_order = PurchaseOrder(
        po_number=po_number,
        status=PurchaseOrderStatus.DRAFT,
        created_by=created_by,
    )

    _populate_purchase_order_header(
        purchase_order,
        request,
    )

    purchase_order.lines = _build_purchase_order_lines(
        db,
        request.lines,
    )

    _calculate_purchase_order_totals(purchase_order)

    save_purchase_order(
        db,
        purchase_order,
    )

    db.commit()
    db.refresh(purchase_order)

    logger.info(
        "Purchase Order %s created successfully.",
        purchase_order.po_number,
    )

    return map_purchase_order(purchase_order)


def update_purchase_order(
    db: Session,
    purchase_order_id: int,
    request: PurchaseOrderUpdateRequest,
    updated_by: int,
) -> PurchaseOrderResponse:

    logger.info(
        "Updating Purchase Order id=%s",
        purchase_order_id,
    )

    purchase_order = _get_purchase_order(
        db,
        purchase_order_id,
    )

    validate_draft_purchase_order(
        purchase_order,
    )

    validate_supplier_exists(
        db,
        request.supplier_id,
    )

    validate_warehouse_exists(
        db,
        request.warehouse_id,
    )

    validate_purchase_order_lines(
        request.lines,
    )

    validate_duplicate_products(
        request.lines,
    )

    validate_expected_delivery_date(
        request.expected_delivery_date,
    )

    _populate_purchase_order_header(
        purchase_order,
        request,
    )

    for request_line in request.lines:

        if request_line.id is None:

            purchase_order.lines.append(
                _create_purchase_order_line(
                    db,
                    request_line,
                )
            )

            continue

        purchase_order_line = get_or_raise(
            _find_purchase_order_line(
                purchase_order,
                request_line.id,
            ),
            PurchaseOrderLineNotFoundException(
                request_line.id,
            ),
        )

        _update_purchase_order_line(
            db,
            purchase_order_line,
            request_line,
        )

    _delete_purchase_order_lines(
        purchase_order,
        request.deleted_line_ids,
    )

    _renumber_purchase_order_lines(
        purchase_order.lines,
    )

    _calculate_purchase_order_totals(
        purchase_order,
    )

    purchase_order.updated_by = updated_by

    db.commit()
    db.refresh(
        purchase_order,
    )

    logger.info(
        "Purchase Order %s updated successfully.",
        purchase_order.po_number,
    )

    return map_purchase_order(
        purchase_order,
    )


def get_purchase_order(
    db: Session,
    purchase_order_id: int,
) -> PurchaseOrderResponse:

    purchase_order = _get_purchase_order(
        db,
        purchase_order_id,
    )

    return map_purchase_order(
        purchase_order,
    )


def search_purchase_orders(
    db: Session,
    request: PurchaseOrderSearchRequest,
):

    logger.info("Searching purchase orders.")

    purchase_orders, total_items = search_purchase_orders(
        db,
        request,
    )

    total_pages = ceil(total_items / request.size) if total_items > 0 else 0

    return PaginatedResponse(
        items=map_purchase_orders(
            purchase_orders,
        ),
        pagination=PaginationMeta(
            page=request.page,
            size=request.size,
            total_items=total_items,
            total_pages=total_pages,
            has_next=request.page < total_pages,
            has_previous=request.page > 1,
        ),
    )


def submit_purchase_order(
    db: Session,
    purchase_order_id: int,
    submitted_by: int,
) -> PurchaseOrderResponse:

    logger.info(
        "Submitting Purchase Order id=%s",
        purchase_order_id,
    )

    purchase_order = _get_purchase_order(
        db,
        purchase_order_id,
    )

    validate_submit_purchase_order(
        purchase_order,
    )

    purchase_order.status = PurchaseOrderStatus.SUBMITTED

    purchase_order.updated_by = submitted_by

    db.commit()
    db.refresh(
        purchase_order,
    )

    logger.info(
        "Purchase Order %s submitted successfully.",
        purchase_order.po_number,
    )

    return map_purchase_order(
        purchase_order,
    )


def approve_purchase_order(
    db: Session,
    purchase_order_id: int,
    approved_by: int,
) -> PurchaseOrderResponse:

    logger.info(
        "Approving Purchase Order id=%s",
        purchase_order_id,
    )

    purchase_order = _get_purchase_order(
        db,
        purchase_order_id,
    )

    validate_approve_purchase_order(
        purchase_order,
    )

    purchase_order.status = PurchaseOrderStatus.APPROVED

    purchase_order.approved_by = approved_by
    purchase_order.updated_by = approved_by

    db.commit()
    db.refresh(
        purchase_order,
    )

    logger.info(
        "Purchase Order %s approved successfully.",
        purchase_order.po_number,
    )

    return map_purchase_order(
        purchase_order,
    )


def reject_purchase_order(
    db: Session,
    purchase_order_id: int,
    rejected_by: int,
) -> PurchaseOrderResponse:

    logger.info(
        "Rejecting Purchase Order id=%s",
        purchase_order_id,
    )

    purchase_order = _get_purchase_order(
        db,
        purchase_order_id,
    )

    validate_reject_purchase_order(
        purchase_order,
    )

    purchase_order.status = PurchaseOrderStatus.REJECTED

    purchase_order.rejected_by = rejected_by
    purchase_order.updated_by = rejected_by

    db.commit()
    db.refresh(
        purchase_order,
    )

    logger.info(
        "Purchase Order %s rejected successfully.",
        purchase_order.po_number,
    )

    return map_purchase_order(
        purchase_order,
    )


def cancel_purchase_order(
    db: Session,
    purchase_order_id: int,
    cancelled_by: int,
) -> PurchaseOrderResponse:

    logger.info(
        "Cancelling Purchase Order id=%s",
        purchase_order_id,
    )

    purchase_order = _get_purchase_order(
        db,
        purchase_order_id,
    )

    validate_cancel_purchase_order(
        purchase_order,
    )

    purchase_order.status = PurchaseOrderStatus.CANCELLED

    purchase_order.cancelled_by = cancelled_by
    purchase_order.updated_by = cancelled_by

    db.commit()
    db.refresh(
        purchase_order,
    )

    logger.info(
        "Purchase Order %s cancelled successfully.",
        purchase_order.po_number,
    )

    return map_purchase_order(
        purchase_order,
    )


def close_purchase_order(
    db: Session,
    purchase_order_id: int,
    closed_by: int,
) -> PurchaseOrderResponse:

    logger.info(
        "Closing Purchase Order id=%s",
        purchase_order_id,
    )

    purchase_order = _get_purchase_order(
        db,
        purchase_order_id,
    )

    validate_close_purchase_order(
        purchase_order,
    )

    purchase_order.status = PurchaseOrderStatus.CLOSED

    purchase_order.closed_by = closed_by
    purchase_order.updated_by = closed_by

    db.commit()
    db.refresh(
        purchase_order,
    )

    logger.info(
        "Purchase Order %s closed successfully.",
        purchase_order.po_number,
    )

    return map_purchase_order(
        purchase_order,
    )
