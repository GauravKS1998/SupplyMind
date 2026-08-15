from __future__ import annotations

from math import ceil

from sqlalchemy.orm import Session

from app.common.entity_utils import get_or_raise
from app.common.pagination import PaginationMeta
from app.common.responses import PaginatedResponse

from app.goods_receipts.enums import GoodsReceiptStatus
from app.goods_receipts.mapper import (
    map_goods_receipt,
    map_goods_receipts,
)
from app.goods_receipts.model import (
    GoodsReceipt,
    GoodsReceiptLine,
)
from app.goods_receipts.repository import (
    find_goods_receipt_by_id,
    search_goods_receipts as search_goods_receipts_repository,
    save_goods_receipt,
)
from app.goods_receipts.validators import (
    validate_accepted_quantity,
    validate_approve_goods_receipt,
    validate_cancel_goods_receipt,
    validate_draft_goods_receipt,
    validate_duplicate_purchase_order_lines,
    validate_goods_receipt_lines,
    validate_product_matches_purchase_order,
    validate_purchase_order_can_receive,
    validate_purchase_order_exists,
    validate_purchase_order_line_exists,
    validate_rejected_quantity,
    validate_remaining_receivable_quantity,
    validate_submit_goods_receipt,
    validate_warehouse_exists,
)

from app.inventory_transactions.enums import (
    InventoryReferenceType,
)
from app.inventories.repository import (
    find_duplicate_inventory,
)

from app.inventories.exceptions import InventoryNotFoundException

from app.inventories.service import _increase_inventory

from app.purchase_orders.model import (
    PurchaseOrder,
    PurchaseOrderLine,
)
from app.purchase_orders.enums import PurchaseOrderStatus

from app.logging.logger import logger

from app.common.document_number.enums import DocumentType
from app.common.document_number.service import get_next_document_number

from .exceptions import (
    GoodsReceiptLineNotFoundException,
    GoodsReceiptNotFoundException,
)

from .schema import (
    GoodsReceiptCreateRequest,
    GoodsReceiptLineCreateRequest,
    GoodsReceiptLineUpdateRequest,
    GoodsReceiptResponse,
    GoodsReceiptSearchRequest,
    GoodsReceiptUpdateRequest,
)


def _validate_goods_receipt_line(
    db: Session,
    purchase_order: PurchaseOrder,
    request_line: GoodsReceiptLineCreateRequest | GoodsReceiptLineUpdateRequest,
) -> PurchaseOrderLine:

    purchase_order_line = validate_purchase_order_line_exists(
        db,
        request_line.purchase_order_line_id,
    )

    if purchase_order_line.purchase_order_id != purchase_order.id:
        raise GoodsReceiptLineNotFoundException(
            request_line.purchase_order_line_id,
        )

    validate_product_matches_purchase_order(
        purchase_order_line,
        request_line,
    )

    validate_accepted_quantity(
        request_line.accepted_quantity,
    )

    validate_rejected_quantity(
        request_line.rejected_quantity,
    )

    validate_remaining_receivable_quantity(
        purchase_order_line,
        request_line.accepted_quantity,
        request_line.rejected_quantity,
    )

    return purchase_order_line


def _create_goods_receipt_line(
    db: Session,
    purchase_order: PurchaseOrder,
    request_line: GoodsReceiptLineCreateRequest | GoodsReceiptLineUpdateRequest,
) -> GoodsReceiptLine:

    purchase_order_line = _validate_goods_receipt_line(
        db,
        purchase_order,
        request_line,
    )

    return GoodsReceiptLine(
        purchase_order_line_id=purchase_order_line.id,
        product_id=purchase_order_line.product_id,
        product_name_snapshot=purchase_order_line.product_name_snapshot,
        product_sku_snapshot=purchase_order_line.product_sku_snapshot,
        batch_number=request_line.batch_number,
        accepted_quantity=request_line.accepted_quantity,
        rejected_quantity=request_line.rejected_quantity,
        remarks=request_line.remarks,
    )


def _update_goods_receipt_line(
    db: Session,
    purchase_order: PurchaseOrder,
    goods_receipt_line: GoodsReceiptLine,
    request_line: GoodsReceiptLineUpdateRequest,
):

    purchase_order_line = _validate_goods_receipt_line(
        db,
        purchase_order,
        request_line,
    )

    if goods_receipt_line.purchase_order_line_id != purchase_order_line.id:
        raise GoodsReceiptLineNotFoundException(
            request_line.purchase_order_line_id,
        )

    goods_receipt_line.batch_number = request_line.batch_number

    goods_receipt_line.accepted_quantity = request_line.accepted_quantity

    goods_receipt_line.rejected_quantity = request_line.rejected_quantity

    goods_receipt_line.remarks = request_line.remarks


def _build_goods_receipt_lines(
    db: Session,
    purchase_order: PurchaseOrder,
    request_lines: list[GoodsReceiptLineCreateRequest],
) -> list[GoodsReceiptLine]:

    goods_receipt_lines = []

    for request_line in request_lines:

        goods_receipt_lines.append(
            _create_goods_receipt_line(
                db,
                purchase_order,
                request_line,
            )
        )

    _renumber_goods_receipt_lines(
        goods_receipt_lines,
    )

    return goods_receipt_lines


def _renumber_goods_receipt_lines(
    goods_receipt_lines: list[GoodsReceiptLine],
):

    for index, line in enumerate(
        goods_receipt_lines,
        start=1,
    ):
        line.line_number = index


def _delete_goods_receipt_lines(
    goods_receipt: GoodsReceipt,
    deleted_line_ids: list[int],
):

    for deleted_line_id in deleted_line_ids:

        goods_receipt_line = get_or_raise(
            _find_goods_receipt_line(
                goods_receipt,
                deleted_line_id,
            ),
            GoodsReceiptLineNotFoundException(
                deleted_line_id,
            ),
        )

        goods_receipt.lines.remove(
            goods_receipt_line,
        )


def _find_goods_receipt_line(
    goods_receipt: GoodsReceipt,
    goods_receipt_line_id: int,
) -> GoodsReceiptLine | None:

    return next(
        (line for line in goods_receipt.lines if line.id == goods_receipt_line_id),
        None,
    )


def _populate_goods_receipt_header(
    goods_receipt: GoodsReceipt,
    request: GoodsReceiptCreateRequest | GoodsReceiptUpdateRequest,
):

    goods_receipt.purchase_order_id = request.purchase_order_id
    goods_receipt.warehouse_id = request.warehouse_id
    goods_receipt.remarks = request.remarks


def _get_goods_receipt(
    db: Session,
    goods_receipt_id: int,
) -> GoodsReceipt:

    return get_or_raise(
        find_goods_receipt_by_id(
            db,
            goods_receipt_id,
        ),
        GoodsReceiptNotFoundException(
            goods_receipt_id,
        ),
    )


def _update_purchase_order_status(
    purchase_order: PurchaseOrder,
):
    total_ordered = sum(line.ordered_quantity for line in purchase_order.lines)

    total_received = sum(line.received_quantity for line in purchase_order.lines)

    if total_received >= total_ordered:
        purchase_order.status = PurchaseOrderStatus.RECEIVED

    elif total_received > 0:
        purchase_order.status = PurchaseOrderStatus.PARTIALLY_RECEIVED


def create_goods_receipt(
    db: Session,
    request: GoodsReceiptCreateRequest,
    created_by: int,
) -> GoodsReceiptResponse:

    logger.info(
        "Creating Goods Receipt for Purchase Order id=%s",
        request.purchase_order_id,
    )

    purchase_order = validate_purchase_order_exists(
        db,
        request.purchase_order_id,
    )

    validate_purchase_order_can_receive(
        purchase_order,
    )

    validate_warehouse_exists(
        db,
        request.warehouse_id,
    )

    validate_goods_receipt_lines(
        request.lines,
    )

    validate_duplicate_purchase_order_lines(
        request.lines,
    )

    grn_number = get_next_document_number(
        db=db,
        document_type=DocumentType.GOODS_RECEIPT,
    )

    goods_receipt = GoodsReceipt(
        grn_number=grn_number,
        purchase_order_id=purchase_order.id,
        warehouse_id=request.warehouse_id,
        status=GoodsReceiptStatus.DRAFT,
        created_by=created_by,
        remarks=request.remarks,
    )

    goods_receipt.lines = _build_goods_receipt_lines(
        db,
        purchase_order,
        request.lines,
    )

    save_goods_receipt(
        db,
        goods_receipt,
    )

    db.commit()
    db.refresh(goods_receipt)

    logger.info(
        "Goods Receipt %s created successfully.",
        goods_receipt.grn_number,
    )

    return map_goods_receipt(
        goods_receipt,
    )


def update_goods_receipt(
    db: Session,
    goods_receipt_id: int,
    request: GoodsReceiptUpdateRequest,
    updated_by: int,
) -> GoodsReceiptResponse:

    logger.info(
        "Updating Goods Receipt id=%s",
        goods_receipt_id,
    )

    goods_receipt = _get_goods_receipt(
        db,
        goods_receipt_id,
    )

    validate_draft_goods_receipt(
        goods_receipt,
    )

    purchase_order = validate_purchase_order_exists(
        db,
        request.purchase_order_id,
    )

    validate_purchase_order_can_receive(
        purchase_order,
    )

    validate_warehouse_exists(
        db,
        request.warehouse_id,
    )

    validate_goods_receipt_lines(
        request.lines,
    )

    validate_duplicate_purchase_order_lines(
        request.lines,
    )

    _populate_goods_receipt_header(
        goods_receipt,
        request,
    )

    for request_line in request.lines:

        if request_line.id is None:

            goods_receipt.lines.append(
                _create_goods_receipt_line(
                    db,
                    purchase_order,
                    request_line,
                )
            )

            continue

        goods_receipt_line = get_or_raise(
            _find_goods_receipt_line(
                goods_receipt,
                request_line.id,
            ),
            GoodsReceiptLineNotFoundException(
                request_line.id,
            ),
        )

        _update_goods_receipt_line(
            db,
            purchase_order,
            goods_receipt_line,
            request_line,
        )

    _delete_goods_receipt_lines(
        goods_receipt,
        request.deleted_line_ids,
    )

    _renumber_goods_receipt_lines(
        goods_receipt.lines,
    )

    goods_receipt.updated_by = updated_by

    db.commit()
    db.refresh(goods_receipt)

    logger.info(
        "Goods Receipt %s updated successfully.",
        goods_receipt.grn_number,
    )

    return map_goods_receipt(
        goods_receipt,
    )


def get_goods_receipt(
    db: Session,
    goods_receipt_id: int,
) -> GoodsReceiptResponse:

    goods_receipt = _get_goods_receipt(
        db,
        goods_receipt_id,
    )

    return map_goods_receipt(
        goods_receipt,
    )


def search_goods_receipts(
    db: Session,
    request: GoodsReceiptSearchRequest,
):

    logger.info("Searching goods receipts.")

    goods_receipts, total_items = search_goods_receipts_repository(
        db,
        request,
    )

    total_pages = ceil(total_items / request.size) if total_items > 0 else 0

    return PaginatedResponse(
        items=map_goods_receipts(
            goods_receipts,
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


def submit_goods_receipt(
    db: Session,
    goods_receipt_id: int,
    submitted_by: int,
) -> GoodsReceiptResponse:

    logger.info(
        "Submitting Goods Receipt id=%s",
        goods_receipt_id,
    )

    goods_receipt = _get_goods_receipt(
        db,
        goods_receipt_id,
    )

    validate_submit_goods_receipt(
        goods_receipt,
    )

    goods_receipt.status = GoodsReceiptStatus.SUBMITTED

    goods_receipt.updated_by = submitted_by

    db.commit()
    db.refresh(goods_receipt)

    logger.info(
        "Goods Receipt %s submitted successfully.",
        goods_receipt.grn_number,
    )

    return map_goods_receipt(
        goods_receipt,
    )


def cancel_goods_receipt(
    db: Session,
    goods_receipt_id: int,
    cancelled_by: int,
) -> GoodsReceiptResponse:

    logger.info(
        "Cancelling Goods Receipt id=%s",
        goods_receipt_id,
    )

    goods_receipt = _get_goods_receipt(
        db,
        goods_receipt_id,
    )

    validate_cancel_goods_receipt(
        goods_receipt,
    )

    goods_receipt.status = GoodsReceiptStatus.CANCELLED

    goods_receipt.cancelled_by = cancelled_by
    goods_receipt.updated_by = cancelled_by

    db.commit()
    db.refresh(goods_receipt)

    logger.info(
        "Goods Receipt %s cancelled successfully.",
        goods_receipt.grn_number,
    )

    return map_goods_receipt(
        goods_receipt,
    )


def approve_goods_receipt(
    db: Session,
    goods_receipt_id: int,
    approved_by: int,
) -> GoodsReceiptResponse:

    logger.info(
        "Approving Goods Receipt id=%s",
        goods_receipt_id,
    )

    goods_receipt = _get_goods_receipt(
        db,
        goods_receipt_id,
    )

    validate_approve_goods_receipt(
        goods_receipt,
    )

    purchase_order = goods_receipt.purchase_order

    for line in goods_receipt.lines:

        inventory = get_or_raise(
            find_duplicate_inventory(
                db,
                line.product_id,
                goods_receipt.warehouse_id,
                line.batch_number,
            ),
            InventoryNotFoundException(
                f"Inventory not found for product '{line.product_id}', "
                f"warehouse '{goods_receipt.warehouse_id}', "
                f"batch '{line.batch_number}'."
            ),
        )

        _increase_inventory(
            db=db,
            inventory=inventory,
            quantity=line.accepted_quantity,
            current_user_id=approved_by,
            reason=f"Goods Receipt {goods_receipt.grn_number} approved.",
            reference_type=InventoryReferenceType.GOODS_RECEIPT,
            reference_id=goods_receipt.id,
        )

        purchase_order_line = line.purchase_order_line

        purchase_order_line.received_quantity += line.accepted_quantity

    _update_purchase_order_status(
        purchase_order,
    )

    goods_receipt.status = GoodsReceiptStatus.APPROVED

    goods_receipt.approved_by = approved_by
    goods_receipt.received_by = approved_by
    goods_receipt.updated_by = approved_by

    db.commit()
    db.refresh(goods_receipt)

    logger.info(
        "Goods Receipt %s approved successfully.",
        goods_receipt.grn_number,
    )

    return map_goods_receipt(
        goods_receipt,
    )
