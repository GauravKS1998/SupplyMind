from decimal import Decimal

from datetime import datetime, timezone

from app.common.entity_utils import get_or_raise
from app.products.repository import find_by_id as find_product_by_id
from app.suppliers.repository import find_by_id as find_supplier_by_id
from app.warehouses.repository import find_by_id as find_warehouse_by_id

from .enums import PurchaseOrderStatus
from .exceptions import (
    PurchaseOrderCannotBeApprovedException,
    PurchaseOrderCannotBeCancelledException,
    PurchaseOrderCannotBeClosedException,
    PurchaseOrderCannotBeModifiedException,
    PurchaseOrderCannotBeRejectedException,
    PurchaseOrderCannotBeSubmittedException,
    PurchaseOrderValidationException,
)
from .model import PurchaseOrder


# Supplier Validation
def validate_supplier_exists(db, supplier_id):

    return get_or_raise(
        find_supplier_by_id(db, supplier_id),
        PurchaseOrderValidationException("Supplier does not exist."),
    )


# Warehouse Validation
def validate_warehouse_exists(db, warehouse_id):

    return get_or_raise(
        find_warehouse_by_id(db, warehouse_id),
        PurchaseOrderValidationException("Warehouse does not exist."),
    )


# Product Validation
def validate_product_exists(db, product_id):

    return get_or_raise(
        find_product_by_id(db, product_id),
        PurchaseOrderValidationException("Product does not exist."),
    )


# Validate Lines Exist
def validate_purchase_order_lines(lines):

    if not lines:
        raise PurchaseOrderValidationException(
            "Purchase Order must contain at least one line."
        )


# Quantity Validation
def validate_ordered_quantity(quantity):

    if quantity <= 0:
        raise PurchaseOrderValidationException(
            "Ordered quantity must be greater than zero."
        )


# Unit Price Validation
def validate_unit_price(price: Decimal):

    if price < Decimal("0"):
        raise PurchaseOrderValidationException("Unit price cannot be negative.")


# Discount Validation
def validate_discount(discount: Decimal):

    if discount < Decimal("0"):
        raise PurchaseOrderValidationException("Discount cannot be negative.")


# Tax Validation
def validate_tax(tax: Decimal):

    if tax < Decimal("0"):
        raise PurchaseOrderValidationException("Tax cannot be negative.")


# Draft Validation
def validate_draft_purchase_order(
    purchase_order: PurchaseOrder,
):

    if purchase_order.status != PurchaseOrderStatus.DRAFT:
        raise PurchaseOrderCannotBeModifiedException(
            "Only draft purchase orders can be modified."
        )


# Submit Validation
def validate_submit_purchase_order(
    purchase_order: PurchaseOrder,
):

    if purchase_order.status != PurchaseOrderStatus.DRAFT:
        raise PurchaseOrderCannotBeSubmittedException(
            "Only draft purchase orders can be submitted."
        )


# Approve Validation
def validate_approve_purchase_order(
    purchase_order: PurchaseOrder,
):

    if purchase_order.status != PurchaseOrderStatus.SUBMITTED:
        raise PurchaseOrderCannotBeApprovedException(
            "Only submitted purchase orders can be approved."
        )


# Reject Validation
def validate_reject_purchase_order(
    purchase_order: PurchaseOrder,
):

    if purchase_order.status != PurchaseOrderStatus.SUBMITTED:
        raise PurchaseOrderCannotBeRejectedException(
            "Only submitted purchase orders can be rejected."
        )


# Cancel Validation
def validate_cancel_purchase_order(
    purchase_order: PurchaseOrder,
):

    if purchase_order.status in (
        PurchaseOrderStatus.RECEIVED,
        PurchaseOrderStatus.CLOSED,
        PurchaseOrderStatus.CANCELLED,
    ):
        raise PurchaseOrderCannotBeCancelledException(
            "Purchase Order cannot be cancelled."
        )


# Close Validation
def validate_close_purchase_order(
    purchase_order: PurchaseOrder,
):

    if purchase_order.status != PurchaseOrderStatus.RECEIVED:
        raise PurchaseOrderCannotBeClosedException(
            "Only fully received purchase orders can be closed."
        )


# Validate Duplicate Products
# A product should not appear twice in the same Purchase Order.
def validate_duplicate_products(lines):

    product_ids = [line.product_id for line in lines]

    if len(product_ids) != len(set(product_ids)):
        raise PurchaseOrderValidationException(
            "Duplicate products are not allowed in a Purchase Order."
        )


# Validate Delivery Date
def validate_expected_delivery_date(expected_delivery_date):

    if expected_delivery_date and expected_delivery_date < datetime.now(timezone.utc):
        raise PurchaseOrderValidationException(
            "Expected delivery date cannot be in the past."
        )
