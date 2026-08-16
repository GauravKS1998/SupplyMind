from app.common.entity_utils import get_or_raise

from app.products.model import Product
from app.products.repository import find_by_id as find_product_by_id

from app.inventories.repository import (
    find_duplicate_inventory,
)

from app.purchase_orders.model import PurchaseOrder

from .enums import SalesOrderStatus
from .exceptions import (
    InsufficientStockException,
    SalesOrderCannotBeCancelledException,
    SalesOrderCannotBeCompletedException,
    SalesOrderCannotBeConfirmedException,
    SalesOrderCannotBeDeliveredException,
    SalesOrderCannotBeDispatchedException,
    SalesOrderCannotBeModifiedException,
    SalesOrderCannotBeReservedException,
    SalesOrderCannotBeReturnedException,
    SalesOrderLineNotFoundException,
    SalesOrderValidationException,
)
from .model import (
    SalesOrder,
    SalesOrderLine,
)


def validate_product_exists(
    db,
    product_id: int,
) -> Product:

    return get_or_raise(
        find_product_by_id(
            db,
            product_id,
        ),
        SalesOrderValidationException(f"Product with id '{product_id}' was not found."),
    )


def validate_ordered_quantity(
    quantity: int,
):
    if quantity <= 0:
        raise SalesOrderValidationException(
            "Ordered quantity must be greater than zero."
        )


def validate_unit_price(
    unit_price,
):
    if unit_price < 0:
        raise SalesOrderValidationException("Unit price cannot be negative.")


def validate_discount(
    discount_amount,
):
    if discount_amount < 0:
        raise SalesOrderValidationException("Discount amount cannot be negative.")


def validate_tax(
    tax_amount,
):
    if tax_amount < 0:
        raise SalesOrderValidationException("Tax amount cannot be negative.")


def validate_sales_order_lines(
    lines,
):
    if not lines:
        raise SalesOrderValidationException(
            "Sales Order must contain at least one line."
        )


def validate_duplicate_products(
    lines,
):
    product_ids = [line.product_id for line in lines]

    if len(product_ids) != len(set(product_ids)):
        raise SalesOrderValidationException(
            "A product cannot appear more than once in a Sales Order."
        )


def validate_draft_sales_order(
    sales_order: SalesOrder,
):
    if sales_order.status != SalesOrderStatus.DRAFT:
        raise SalesOrderCannotBeModifiedException(
            "Only draft Sales Orders can be modified."
        )


def validate_confirm_sales_order(
    sales_order: SalesOrder,
):
    if sales_order.status != SalesOrderStatus.DRAFT:
        raise SalesOrderCannotBeConfirmedException(
            "Only draft Sales Orders can be confirmed."
        )


def validate_reserve_sales_order(
    sales_order: SalesOrder,
):
    if sales_order.status != SalesOrderStatus.CONFIRMED:
        raise SalesOrderCannotBeReservedException(
            "Only confirmed Sales Orders can be reserved."
        )


def validate_dispatch_sales_order(
    sales_order: SalesOrder,
):
    if sales_order.status != SalesOrderStatus.RESERVED:
        raise SalesOrderCannotBeDispatchedException(
            "Only reserved Sales Orders can be dispatched."
        )


def validate_deliver_sales_order(
    sales_order: SalesOrder,
):
    if sales_order.status != SalesOrderStatus.DISPATCHED:
        raise SalesOrderCannotBeDeliveredException(
            "Only dispatched Sales Orders can be delivered."
        )


def validate_complete_sales_order(
    sales_order: SalesOrder,
):
    if sales_order.status != SalesOrderStatus.DELIVERED:
        raise SalesOrderCannotBeCompletedException(
            "Only delivered Sales Orders can be completed."
        )


def validate_cancel_sales_order(
    sales_order: SalesOrder,
):
    if sales_order.status not in {
        SalesOrderStatus.DRAFT,
        SalesOrderStatus.CONFIRMED,
        SalesOrderStatus.RESERVED,
    }:
        raise SalesOrderCannotBeCancelledException(
            "Sales Order cannot be cancelled in its current state."
        )


def validate_return_sales_order(
    sales_order: SalesOrder,
):
    if sales_order.status not in {
        SalesOrderStatus.DELIVERED,
        SalesOrderStatus.COMPLETED,
    }:
        raise SalesOrderCannotBeReturnedException(
            "Only delivered or completed Sales Orders can be returned."
        )


def validate_sufficient_stock(
    available_quantity: int,
    requested_quantity: int,
):
    if available_quantity < requested_quantity:
        raise InsufficientStockException("Insufficient available inventory.")


def find_sales_order_line(
    sales_order: SalesOrder,
    sales_order_line_id: int,
) -> SalesOrderLine | None:

    return next(
        (line for line in sales_order.lines if line.id == sales_order_line_id),
        None,
    )
