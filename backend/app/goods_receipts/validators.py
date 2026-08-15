from sqlalchemy.orm import Session

from app.common.entity_utils import get_or_raise

from app.goods_receipts.enums import GoodsReceiptStatus
from app.goods_receipts.exceptions import (
    DuplicateProductException,
    GoodsReceiptCannotBeApprovedException,
    GoodsReceiptCannotBeCancelledException,
    GoodsReceiptCannotBeModifiedException,
    GoodsReceiptCannotBeSubmittedException,
    GoodsReceiptHasNoLinesException,
    InvalidAcceptedQuantityException,
    InvalidRejectedQuantityException,
    PurchaseOrderNotEligibleForReceivingException,
    ReceivedQuantityExceededException,
    GoodsReceiptValidationException,
)

from app.goods_receipts.model import GoodsReceipt

from app.purchase_orders.enums import PurchaseOrderStatus
from app.purchase_orders.exceptions import (
    PurchaseOrderNotFoundException,
    PurchaseOrderLineNotFoundException,
)
from app.purchase_orders.model import (
    PurchaseOrder,
    PurchaseOrderLine,
)
from app.purchase_orders.repository import (
    find_purchase_order_by_id,
    find_purchase_order_line_by_id,
)

from app.warehouses.exceptions import WarehouseNotFoundException
from app.warehouses.repository import find_by_id as find_warehouse_by_id


def validate_purchase_order_exists(
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


def validate_warehouse_exists(
    db: Session,
    warehouse_id: int,
):

    return get_or_raise(
        find_warehouse_by_id(
            db,
            warehouse_id,
        ),
        WarehouseNotFoundException(
            warehouse_id,
        ),
    )


def validate_purchase_order_line_exists(
    db: Session,
    purchase_order_line_id: int,
) -> PurchaseOrderLine:

    return get_or_raise(
        find_purchase_order_line_by_id(
            db,
            purchase_order_line_id,
        ),
        PurchaseOrderLineNotFoundException(
            purchase_order_line_id,
        ),
    )


def validate_goods_receipt_lines(
    lines,
):

    if not lines:
        raise GoodsReceiptHasNoLinesException(
            "Goods Receipt must contain at least one line."
        )


def validate_duplicate_purchase_order_lines(
    lines,
):

    purchase_order_line_ids = [line.purchase_order_line_id for line in lines]

    if len(purchase_order_line_ids) != len(set(purchase_order_line_ids)):
        raise DuplicateProductException(
            "Duplicate Purchase Order Lines are not allowed."
        )


def validate_accepted_quantity(
    accepted_quantity: int,
):

    if accepted_quantity <= 0:
        raise InvalidAcceptedQuantityException(
            "Accepted quantity must be greater than zero."
        )


def validate_rejected_quantity(
    rejected_quantity: int,
):

    if rejected_quantity < 0:
        raise InvalidRejectedQuantityException("Rejected quantity cannot be negative.")


def validate_product_matches_purchase_order(
    purchase_order_line: PurchaseOrderLine,
    product_id: int,
):

    if purchase_order_line.product_id != product_id:
        raise GoodsReceiptValidationException(
            "Product does not match the Purchase Order Line."
        )


def validate_remaining_receivable_quantity(
    purchase_order_line: PurchaseOrderLine,
    accepted_quantity: int,
    rejected_quantity: int,
):

    remaining_quantity = (
        purchase_order_line.ordered_quantity - purchase_order_line.received_quantity
    )

    if accepted_quantity + rejected_quantity > remaining_quantity:
        raise ReceivedQuantityExceededException(
            "Received quantity exceeds the remaining receivable quantity."
        )


def validate_purchase_order_can_receive(
    purchase_order: PurchaseOrder,
):

    if purchase_order.status not in (
        PurchaseOrderStatus.APPROVED,
        PurchaseOrderStatus.PARTIALLY_RECEIVED,
    ):
        raise PurchaseOrderNotEligibleForReceivingException(
            "Purchase Order is not eligible for receiving."
        )


def validate_draft_goods_receipt(
    goods_receipt: GoodsReceipt,
):

    if goods_receipt.status != GoodsReceiptStatus.DRAFT:
        raise GoodsReceiptCannotBeModifiedException(
            "Only Draft Goods Receipts can be modified."
        )


def validate_submit_goods_receipt(
    goods_receipt: GoodsReceipt,
):

    if goods_receipt.status != GoodsReceiptStatus.DRAFT:
        raise GoodsReceiptCannotBeSubmittedException(
            "Only Draft Goods Receipts can be submitted."
        )


def validate_approve_goods_receipt(
    goods_receipt: GoodsReceipt,
):

    if goods_receipt.status != GoodsReceiptStatus.SUBMITTED:
        raise GoodsReceiptCannotBeApprovedException(
            "Only Submitted Goods Receipts can be approved."
        )


def validate_cancel_goods_receipt(
    goods_receipt: GoodsReceipt,
):

    if goods_receipt.status not in (
        GoodsReceiptStatus.DRAFT,
        GoodsReceiptStatus.SUBMITTED,
    ):
        raise GoodsReceiptCannotBeCancelledException(
            "Only Draft or Submitted Goods Receipts can be cancelled."
        )
