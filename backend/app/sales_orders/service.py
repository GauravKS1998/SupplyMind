from sqlalchemy.orm import Session

from datetime import datetime, timezone

from app.sales_orders.enums import SalesOrderStatus
from .exceptions import (
    InsufficientStockException,
    SalesOrderAlreadyExistsException,
    SalesOrderCannotBeCancelledException,
    SalesOrderFailException,
    SalesOrderNotDeliveredException,
    SalesOrderNotDispatchedException,
    SalesOrderNotDraftedException,
    SalesOrderNotConfirmedException,
    SalesOrderNotFoundException,
    SalesOrderNotReservedException,
)
from app.products.exceptions import ProductNotFoundException
from app.inventories.exceptions import InventoryNotFoundException

from .model import SalesOrder
from .schema import SalesOrderCreateRequest, SalesOrderResponse

from .repository import save, find_all, find_by_id, find_by_so_number

from app.products.repository import find_by_id as find_product_by_id
from app.inventories.repository import find_by_product_and_warehouse

from app.logging.logger import logger


def map_sales_order(sales_order: SalesOrder):
    return SalesOrderResponse(
        id=sales_order.id,
        so_number=sales_order.so_number,
        product_id=sales_order.product_id,
        product_name=sales_order.product.name,
        product_sku=sales_order.product.sku,
        warehouse_id=sales_order.warehouse_id,
        warehouse_name=sales_order.warehouse.name,
        quantity=sales_order.quantity,
        total_price=sales_order.total_price,
        sold_at=sales_order.sold_at,
        created_by=sales_order.created_by,
        status=sales_order.status,
        customer_id=sales_order.customer_id,
    )


def get_all_sales_orders(db: Session):
    sales_orders = find_all(db)

    return [map_sales_order(order) for order in sales_orders]


def create_draft_sales_order(
    db: Session, request: SalesOrderCreateRequest, current_user_id: int
):
    existing_so = find_by_so_number(db, request.so_number)

    if existing_so:
        raise SalesOrderAlreadyExistsException("SO already exists")

    product = find_product_by_id(db, request.product_id)

    if not product:
        raise ProductNotFoundException("Product not found")

    total_price = product.price * request.quantity

    try:
        sales_order = SalesOrder(
            so_number=request.so_number,
            product_id=request.product_id,
            warehouse_id=request.warehouse_id,
            customer_id=request.customer_id,
            quantity=request.quantity,
            total_price=total_price,
            created_by=current_user_id,
            status=SalesOrderStatus.DRAFT,
        )

        saved_order = save(db, sales_order)

        db.commit()
        db.refresh(saved_order)

        logger.info(f"Sales order {saved_order.id} drafted")

        return map_sales_order(saved_order)

    except Exception:
        db.rollback()
        raise SalesOrderFailException("Failed to create sales order")


def confirm_sales_order(db: Session, sales_order_id: int, current_user_id: int):
    sales_order = find_by_id(db, sales_order_id)

    if not sales_order:
        raise SalesOrderNotFoundException("Sales order not found")

    if sales_order.status != SalesOrderStatus.DRAFT:
        raise SalesOrderNotDraftedException("Only draft SO can be submitted")

    inventory = find_by_product_and_warehouse(
        db, sales_order.product_id, sales_order.warehouse_id
    )

    if inventory.available_quantity < sales_order.quantity:
        raise InsufficientStockException("Insufficient stock")

    try:
        sales_order.status = SalesOrderStatus.CONFIRMED
        sales_order.confirmed_by = current_user_id
        sales_order.updated_by = current_user_id
        sales_order.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(sales_order)

        logger.info(f"Sales order {sales_order.id} confirmed")

        return {"message": "Sales order confirmed"}

    except Exception:
        db.rollback()
        raise SalesOrderFailException("Failed to confirm sales order")


def reserve_sales_order(db: Session, sales_order_id: int, current_user_id: int):
    sales_order = find_by_id(db, sales_order_id)

    if not sales_order:
        raise SalesOrderNotFoundException("Sales order not found")

    if sales_order.status != SalesOrderStatus.CONFIRMED:
        raise SalesOrderNotConfirmedException("Only confirmed SO can be reserved")

    inventory = find_by_product_and_warehouse(
        db, sales_order.product_id, sales_order.warehouse_id
    )

    if inventory.available_quantity < sales_order.quantity:
        raise InsufficientStockException("Insufficient stock")

    try:
        inventory.reserved_quantity += sales_order.quantity
        inventory.available_quantity -= sales_order.quantity

        sales_order.status = SalesOrderStatus.RESERVED
        sales_order.updated_by = current_user_id
        sales_order.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(sales_order)

        logger.info(f"Sales order {sales_order.id} reserved")

        return {"message": "Sales order reserved"}

    except Exception:
        db.rollback()
        raise SalesOrderFailException("Failed to reserve sales order")


def dispatch_sales_order(db: Session, sales_order_id: int, current_user_id: int):
    sales_order = find_by_id(db, sales_order_id)

    if not sales_order:
        raise SalesOrderNotFoundException("Sales order not found")

    if sales_order.status != SalesOrderStatus.RESERVED:
        raise SalesOrderNotReservedException("Only reserved SO can be dispatched")

    inventory = find_by_product_and_warehouse(
        db, sales_order.product_id, sales_order.warehouse_id
    )

    try:
        inventory.quantity -= sales_order.quantity
        inventory.reserved_quantity -= sales_order.quantity

        sales_order.status = SalesOrderStatus.DISPATCHED
        sales_order.dispatched_by = current_user_id
        sales_order.updated_by = current_user_id
        sales_order.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(sales_order)

        logger.info(f"Sales order {sales_order.id} dispatched")

        return {"message": "Sales order dispatched"}

    except Exception:
        db.rollback()
        raise SalesOrderFailException("Failed to dispatch sales order")


def deliver_sales_order(db: Session, sales_order_id: int, current_user_id: int):
    sales_order = find_by_id(db, sales_order_id)

    if not sales_order:
        raise SalesOrderNotFoundException("Sales order not found")

    if sales_order.status != SalesOrderStatus.DISPATCHED:
        raise SalesOrderNotDispatchedException("Only dispatched SO can be delivered")

    try:
        sales_order.status = SalesOrderStatus.DELIVERED
        sales_order.delivered_by = current_user_id
        sales_order.delivered_at = datetime.now(timezone.utc)
        sales_order.updated_by = current_user_id
        sales_order.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(sales_order)

        logger.info(f"Sales order {sales_order.id} delivered")

        return {"message": "Sales order delivered"}

    except Exception:
        db.rollback()
        raise SalesOrderFailException("Failed to deliver sales order")


def complete_sales_order(db: Session, sales_order_id: int, current_user_id: int):
    sales_order = find_by_id(db, sales_order_id)

    if not sales_order:
        raise SalesOrderNotFoundException("Sales order not found")

    if sales_order.status != SalesOrderStatus.DELIVERED:
        raise SalesOrderNotDeliveredException("Only delivered SO can be completed")

    try:
        sales_order.status = SalesOrderStatus.COMPLETED
        sales_order.completed_by = current_user_id
        sales_order.completed_at = datetime.now(timezone.utc)
        sales_order.updated_by = current_user_id
        sales_order.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(sales_order)

        logger.info(f"Sales order {sales_order.id} completed")

        return {"message": "Sales order completed"}

    except Exception:
        db.rollback()
        raise SalesOrderFailException("Failed to complete sales order")


def cancel_sales_order(db: Session, sales_order_id: int, current_user_id: int):
    sales_order = find_by_id(db, sales_order_id)

    if not sales_order:
        raise SalesOrderNotFoundException("Sales order not found")

    if sales_order.status not in {
        SalesOrderStatus.DRAFT,
        SalesOrderStatus.CONFIRMED,
        SalesOrderStatus.RESERVED,
    }:
        raise SalesOrderCannotBeCancelledException(
            "Sales order cannot be cancelled in current state"
        )

    inventory = find_by_product_and_warehouse(
        db, sales_order.product_id, sales_order.warehouse_id
    )

    if not inventory:
        raise InventoryNotFoundException("Inventory not found")

    try:
        if sales_order.status == SalesOrderStatus.RESERVED:
            inventory.reserved_quantity -= sales_order.quantity
            inventory.available_quantity += sales_order.quantity

        sales_order.status = SalesOrderStatus.CANCELLED
        sales_order.cancelled_by = current_user_id
        sales_order.updated_by = current_user_id
        sales_order.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(sales_order)

        logger.info(f"Sales order {sales_order.id} cancelled")

        return {"message": "Sales order cancelled successfully"}

    except Exception:
        db.rollback()
        raise SalesOrderFailException("Failed to cancel sales order")


def return_sales_order(db: Session, sales_order_id: int, current_user_id: int):
    sales_order = find_by_id(db, sales_order_id)

    if not sales_order:
        raise SalesOrderNotFoundException("Sales order not found")

    if sales_order.status not in {
        SalesOrderStatus.DELIVERED,
        SalesOrderStatus.COMPLETED,
    }:
        raise SalesOrderFailException("Only delivered/completed SO can be returned")

    inventory = find_by_product_and_warehouse(
        db, sales_order.product_id, sales_order.warehouse_id
    )

    try:
        inventory.quantity += sales_order.quantity
        inventory.available_quantity += sales_order.quantity

        sales_order.status = SalesOrderStatus.RETURNED
        sales_order.returned_by = current_user_id
        sales_order.returned_at = datetime.now(timezone.utc)
        sales_order.updated_by = current_user_id
        sales_order.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(sales_order)

        logger.info(f"Sales order {sales_order.id} returned")

        return {"message": "Sales order returned"}

    except Exception:
        db.rollback()
        raise SalesOrderFailException("Failed to return sales order")
