from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from math import ceil

from sqlalchemy.orm import Session

from app.common.entity_utils import get_or_raise
from app.common.pagination import PaginationMeta
from app.common.responses import PaginatedResponse

from app.common.document_number.enums import DocumentType
from app.common.document_number.service import get_next_document_number

from app.inventory_transactions.enums import InventoryReferenceType
from app.inventories.repository import (
    find_available_inventory_for_product,
    find_by_id as find_inventory_by_id,
)
from app.inventories.service import (
    reserve_inventory_transaction,
    release_inventory_transaction,
    increase_inventory_transaction,
    decrease_inventory_transaction,
)

from app.products.model import Product

from app.sales_orders.enums import SalesOrderStatus
from app.sales_orders.exceptions import (
    SalesOrderLineNotFoundException,
    SalesOrderNotFoundException,
    SalesOrderValidationException,
)

from app.sales_orders.mapper import (
    map_sales_order,
    map_sales_orders,
)

from app.sales_orders.model import (
    SalesOrder,
    SalesOrderLine,
)

from app.sales_orders.repository import (
    find_sales_order_by_id,
    save_sales_order,
    search_sales_orders as find_sales_orders,
)

from app.sales_orders.schema import (
    SalesOrderCreateRequest,
    SalesOrderLineCreateRequest,
    SalesOrderLineUpdateRequest,
    SalesOrderResponse,
    SalesOrderSearchRequest,
    SalesOrderUpdateRequest,
)

from app.sales_orders.validators import (
    validate_cancel_sales_order,
    validate_complete_sales_order,
    validate_confirm_sales_order,
    validate_deliver_sales_order,
    validate_discount,
    validate_draft_sales_order,
    validate_duplicate_products,
    validate_ordered_quantity,
    validate_product_exists,
    validate_reserve_sales_order,
    validate_return_sales_order,
    validate_sales_order_lines,
    validate_tax,
    validate_unit_price,
    validate_dispatch_sales_order,
)

from app.logging.logger import logger


def _calculate_sales_order_totals(
    sales_order: SalesOrder,
):
    subtotal = Decimal("0.00")
    discount_total = Decimal("0.00")
    tax_total = Decimal("0.00")

    for line in sales_order.lines:

        line.line_total = (
            (line.unit_price * line.ordered_quantity)
            - line.discount_amount
            + line.tax_amount
        )

        subtotal += line.unit_price * line.ordered_quantity

        discount_total += line.discount_amount
        tax_total += line.tax_amount

    sales_order.subtotal = subtotal
    sales_order.discount_total = discount_total
    sales_order.tax_total = tax_total
    sales_order.grand_total = subtotal - discount_total + tax_total


def _create_sales_order_line(
    db: Session,
    request_line: SalesOrderLineCreateRequest | SalesOrderLineUpdateRequest,
) -> SalesOrderLine:

    product: Product = validate_product_exists(
        db,
        request_line.product_id,
    )

    validate_ordered_quantity(
        request_line.ordered_quantity,
    )

    validate_unit_price(
        request_line.unit_price,
    )

    validate_discount(
        request_line.discount_amount,
    )

    validate_tax(
        request_line.tax_amount,
    )

    return SalesOrderLine(
        product_id=product.id,
        product_name_snapshot=product.name,
        product_sku_snapshot=product.sku,
        ordered_quantity=request_line.ordered_quantity,
        unit_price=request_line.unit_price,
        discount_amount=request_line.discount_amount,
        tax_amount=request_line.tax_amount,
        line_total=Decimal("0.00"),
        remarks=request_line.remarks,
    )


def _update_sales_order_line(
    db: Session,
    sales_order_line: SalesOrderLine,
    request_line: SalesOrderLineUpdateRequest,
):

    product: Product = validate_product_exists(
        db,
        request_line.product_id,
    )

    validate_ordered_quantity(
        request_line.ordered_quantity,
    )

    validate_unit_price(
        request_line.unit_price,
    )

    validate_discount(
        request_line.discount_amount,
    )

    validate_tax(
        request_line.tax_amount,
    )

    sales_order_line.product_id = product.id

    sales_order_line.product_name_snapshot = product.name

    sales_order_line.product_sku_snapshot = product.sku

    sales_order_line.ordered_quantity = request_line.ordered_quantity

    sales_order_line.unit_price = request_line.unit_price

    sales_order_line.discount_amount = request_line.discount_amount

    sales_order_line.tax_amount = request_line.tax_amount

    sales_order_line.remarks = request_line.remarks


def _find_sales_order_line(
    sales_order: SalesOrder,
    sales_order_line_id: int,
) -> SalesOrderLine | None:

    return next(
        (line for line in sales_order.lines if line.id == sales_order_line_id),
        None,
    )


def _delete_sales_order_lines(
    sales_order: SalesOrder,
    deleted_line_ids: list[int],
):

    for deleted_line_id in deleted_line_ids:

        sales_order_line = get_or_raise(
            _find_sales_order_line(
                sales_order,
                deleted_line_id,
            ),
            SalesOrderLineNotFoundException(
                deleted_line_id,
            ),
        )

        sales_order.lines.remove(
            sales_order_line,
        )


def _renumber_sales_order_lines(
    sales_order_lines: list[SalesOrderLine],
):

    for index, line in enumerate(
        sales_order_lines,
        start=1,
    ):
        line.line_number = index


def _populate_sales_order_header(
    sales_order: SalesOrder,
    request: SalesOrderCreateRequest | SalesOrderUpdateRequest,
):

    sales_order.customer_id = request.customer_id
    sales_order.warehouse_id = request.warehouse_id
    sales_order.remarks = request.remarks


def _get_sales_order(
    db: Session,
    sales_order_id: int,
) -> SalesOrder:

    return get_or_raise(
        find_sales_order_by_id(
            db,
            sales_order_id,
        ),
        SalesOrderNotFoundException(
            f"Sales Order with id '{sales_order_id}' was not found."
        ),
    )


def create_sales_order(
    db: Session,
    request: SalesOrderCreateRequest,
    created_by: int,
) -> SalesOrderResponse:

    logger.info(
        "Creating Sales Order for customer_id=%s",
        request.customer_id,
    )

    validate_sales_order_lines(
        request.lines,
    )

    validate_duplicate_products(
        request.lines,
    )

    so_number = get_next_document_number(
        db=db,
        document_type=DocumentType.SALES_ORDER,
    )

    sales_order = SalesOrder(
        so_number=so_number,
        status=SalesOrderStatus.DRAFT,
        created_by=created_by,
    )

    _populate_sales_order_header(
        sales_order,
        request,
    )

    sales_order.lines = [
        _create_sales_order_line(
            db,
            request_line,
        )
        for request_line in request.lines
    ]

    _renumber_sales_order_lines(
        sales_order.lines,
    )

    _calculate_sales_order_totals(
        sales_order,
    )

    save_sales_order(
        db,
        sales_order,
    )

    db.commit()
    db.refresh(
        sales_order,
    )

    logger.info(
        "Sales Order %s created successfully.",
        sales_order.so_number,
    )

    return map_sales_order(
        sales_order,
    )


def update_sales_order(
    db: Session,
    sales_order_id: int,
    request: SalesOrderUpdateRequest,
    updated_by: int,
) -> SalesOrderResponse:

    logger.info(
        "Updating Sales Order id=%s",
        sales_order_id,
    )

    sales_order = _get_sales_order(
        db,
        sales_order_id,
    )

    validate_draft_sales_order(
        sales_order,
    )

    validate_sales_order_lines(
        request.lines,
    )

    validate_duplicate_products(
        request.lines,
    )

    _populate_sales_order_header(
        sales_order,
        request,
    )

    for request_line in request.lines:

        if request_line.id is None:

            sales_order.lines.append(
                _create_sales_order_line(
                    db,
                    request_line,
                )
            )

            continue

        sales_order_line = get_or_raise(
            _find_sales_order_line(
                sales_order,
                request_line.id,
            ),
            SalesOrderLineNotFoundException(
                request_line.id,
            ),
        )

        _update_sales_order_line(
            db,
            sales_order_line,
            request_line,
        )

    _delete_sales_order_lines(
        sales_order,
        request.deleted_line_ids,
    )

    _renumber_sales_order_lines(
        sales_order.lines,
    )

    _calculate_sales_order_totals(
        sales_order,
    )

    sales_order.updated_by = updated_by

    db.commit()
    db.refresh(
        sales_order,
    )

    logger.info(
        "Sales Order %s updated successfully.",
        sales_order.so_number,
    )

    return map_sales_order(
        sales_order,
    )


def get_sales_order(
    db: Session,
    sales_order_id: int,
) -> SalesOrderResponse:

    sales_order = _get_sales_order(
        db,
        sales_order_id,
    )

    return map_sales_order(
        sales_order,
    )


def search_sales_orders(
    db: Session,
    request: SalesOrderSearchRequest,
):

    logger.info("Searching sales orders.")

    sales_orders, total_items = find_sales_orders(
        db,
        request,
    )

    total_pages = ceil(total_items / request.size) if total_items > 0 else 0

    return PaginatedResponse(
        items=map_sales_orders(
            sales_orders,
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


def confirm_sales_order(
    db: Session,
    sales_order_id: int,
    confirmed_by: int,
) -> SalesOrderResponse:

    logger.info(
        "Confirming Sales Order id=%s",
        sales_order_id,
    )

    sales_order = _get_sales_order(
        db,
        sales_order_id,
    )

    validate_confirm_sales_order(
        sales_order,
    )

    sales_order.status = SalesOrderStatus.CONFIRMED

    sales_order.confirmed_by = confirmed_by
    sales_order.updated_by = confirmed_by

    db.commit()
    db.refresh(
        sales_order,
    )

    logger.info(
        "Sales Order %s confirmed successfully.",
        sales_order.so_number,
    )

    return map_sales_order(
        sales_order,
    )


def reserve_sales_order(
    db: Session,
    sales_order_id: int,
    reserved_by: int,
) -> SalesOrderResponse:

    logger.info(
        "Reserving Sales Order id=%s",
        sales_order_id,
    )

    sales_order = _get_sales_order(
        db,
        sales_order_id,
    )

    validate_reserve_sales_order(
        sales_order,
    )

    for line in sales_order.lines:

        inventory = get_or_raise(
            find_available_inventory_for_product(
                db=db,
                product_id=line.product_id,
                warehouse_id=sales_order.warehouse_id,
                required_quantity=line.ordered_quantity,
            ),
            SalesOrderValidationException(
                f"Insufficient available inventory for "
                f"product '{line.product_id}' in "
                f"warehouse '{sales_order.warehouse_id}'."
            ),
        )

        reserve_inventory_transaction(
            db=db,
            inventory=inventory,
            quantity=line.ordered_quantity,
            current_user_id=reserved_by,
            reason=(f"Sales Order " f"{sales_order.so_number} reservation."),
            reference_type=InventoryReferenceType.SALES_ORDER,
            reference_id=sales_order.id,
        )

        line.inventory_id = inventory.id

    sales_order.status = SalesOrderStatus.RESERVED

    sales_order.updated_by = reserved_by

    db.commit()

    db.refresh(
        sales_order,
    )

    logger.info(
        "Sales Order %s reserved successfully.",
        sales_order.so_number,
    )

    return map_sales_order(
        sales_order,
    )


def deliver_sales_order(
    db: Session,
    sales_order_id: int,
    delivered_by: int,
) -> SalesOrderResponse:

    logger.info(
        "Delivering Sales Order id=%s",
        sales_order_id,
    )

    sales_order = _get_sales_order(
        db,
        sales_order_id,
    )

    validate_deliver_sales_order(
        sales_order,
    )

    sales_order.status = SalesOrderStatus.DELIVERED

    sales_order.delivered_by = delivered_by
    sales_order.updated_by = delivered_by
    sales_order.delivered_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(sales_order)

    logger.info(
        "Sales Order %s delivered successfully.",
        sales_order.so_number,
    )

    return map_sales_order(
        sales_order,
    )


def complete_sales_order(
    db: Session,
    sales_order_id: int,
    completed_by: int,
) -> SalesOrderResponse:

    logger.info(
        "Completing Sales Order id=%s",
        sales_order_id,
    )

    sales_order = _get_sales_order(
        db,
        sales_order_id,
    )

    validate_complete_sales_order(
        sales_order,
    )

    sales_order.status = SalesOrderStatus.COMPLETED

    sales_order.completed_by = completed_by
    sales_order.updated_by = completed_by
    sales_order.completed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(sales_order)

    logger.info(
        "Sales Order %s completed successfully.",
        sales_order.so_number,
    )

    return map_sales_order(
        sales_order,
    )


def cancel_sales_order(
    db: Session,
    sales_order_id: int,
    cancelled_by: int,
) -> SalesOrderResponse:

    logger.info(
        "Cancelling Sales Order id=%s",
        sales_order_id,
    )

    sales_order = _get_sales_order(
        db,
        sales_order_id,
    )

    validate_cancel_sales_order(
        sales_order,
    )

    if sales_order.status == SalesOrderStatus.RESERVED:

        for line in sales_order.lines:

            if line.inventory_id is None:
                raise SalesOrderValidationException(
                    f"Inventory allocation is missing for "
                    f"Sales Order Line '{line.id}'."
                )

            inventory = get_or_raise(
                find_inventory_by_id(
                    db,
                    line.inventory_id,
                ),
                SalesOrderValidationException(
                    f"Inventory with id " f"'{line.inventory_id}' was not found."
                ),
            )

            release_inventory_transaction(
                db=db,
                inventory=inventory,
                quantity=line.ordered_quantity,
                current_user_id=cancelled_by,
                reason=(f"Sales Order " f"{sales_order.so_number} cancelled."),
                reference_type=InventoryReferenceType.SALES_ORDER,
                reference_id=sales_order.id,
            )

    sales_order.status = SalesOrderStatus.CANCELLED

    sales_order.cancelled_by = cancelled_by
    sales_order.updated_by = cancelled_by

    db.commit()

    db.refresh(
        sales_order,
    )

    logger.info(
        "Sales Order %s cancelled successfully.",
        sales_order.so_number,
    )

    return map_sales_order(
        sales_order,
    )


def return_sales_order(
    db: Session,
    sales_order_id: int,
    returned_by: int,
) -> SalesOrderResponse:

    logger.info(
        "Returning Sales Order id=%s",
        sales_order_id,
    )

    sales_order = _get_sales_order(
        db,
        sales_order_id,
    )

    validate_return_sales_order(
        sales_order,
    )

    for line in sales_order.lines:

        if line.inventory_id is None:
            raise SalesOrderValidationException(
                f"Inventory allocation is missing for " f"Sales Order Line '{line.id}'."
            )

        inventory = get_or_raise(
            find_inventory_by_id(
                db,
                line.inventory_id,
            ),
            SalesOrderValidationException(
                f"Inventory with id " f"'{line.inventory_id}' was not found."
            ),
        )

        increase_inventory_transaction(
            db=db,
            inventory=inventory,
            quantity=line.ordered_quantity,
            current_user_id=returned_by,
            reason=(f"Sales Order " f"{sales_order.so_number} returned."),
            reference_type=InventoryReferenceType.SALES_ORDER,
            reference_id=sales_order.id,
        )

    sales_order.status = SalesOrderStatus.RETURNED

    sales_order.returned_by = returned_by
    sales_order.updated_by = returned_by
    sales_order.returned_at = datetime.now(timezone.utc)

    db.commit()

    db.refresh(
        sales_order,
    )

    logger.info(
        "Sales Order %s returned successfully.",
        sales_order.so_number,
    )

    return map_sales_order(
        sales_order,
    )


def dispatch_sales_order(
    db: Session,
    sales_order_id: int,
    dispatched_by: int,
) -> SalesOrderResponse:

    logger.info(
        "Dispatching Sales Order id=%s",
        sales_order_id,
    )

    sales_order = _get_sales_order(
        db,
        sales_order_id,
    )

    validate_dispatch_sales_order(
        sales_order,
    )

    for line in sales_order.lines:

        if line.inventory_id is None:
            raise SalesOrderValidationException(
                f"Inventory allocation is missing for " f"Sales Order Line '{line.id}'."
            )

        inventory = get_or_raise(
            find_inventory_by_id(
                db,
                line.inventory_id,
            ),
            SalesOrderValidationException(
                f"Inventory with id " f"'{line.inventory_id}' was not found."
            ),
        )

        decrease_inventory_transaction(
            db=db,
            inventory=inventory,
            quantity=line.ordered_quantity,
            current_user_id=dispatched_by,
            release_reserved=True,
            reason=(f"Sales Order " f"{sales_order.so_number} dispatched."),
            reference_type=InventoryReferenceType.SALES_ORDER,
            reference_id=sales_order.id,
        )

    sales_order.status = SalesOrderStatus.DISPATCHED

    sales_order.dispatched_by = dispatched_by
    sales_order.updated_by = dispatched_by

    db.commit()

    db.refresh(
        sales_order,
    )

    logger.info(
        "Sales Order %s dispatched successfully.",
        sales_order.so_number,
    )

    return map_sales_order(
        sales_order,
    )
