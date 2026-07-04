from sqlalchemy.orm import Session

from .model import SalesOrder
from .schema import SalesOrderCreateRequest, SalesOrderResponse

from .repository import save, find_all

from app.products.repository import find_by_id as find_product_by_id
from app.inventories.repository import find_by_product_and_warehouse


def map_sales_order(sales_order: SalesOrder):
    return SalesOrderResponse(
        id=sales_order.id,
        product_id=sales_order.product_id,
        product_name=sales_order.product.name,
        product_sku=sales_order.product.sku,
        warehouse_id=sales_order.warehouse_id,
        warehouse_name=sales_order.warehouse.name,
        quantity=sales_order.quantity,
        total_price=sales_order.total_price,
        sold_at=sales_order.sold_at,
    )


def create_sales_order(db: Session, request: SalesOrderCreateRequest):
    product = find_product_by_id(db, request.product_id)

    if not product:
        return {"message": "Product not found"}

    inventory = find_by_product_and_warehouse(
        db, request.product_id, request.warehouse_id
    )

    if not inventory:
        return {"message": "Inventoory not found"}

    if inventory.quantity < request.quantity:
        return {"message": "Insufficient stock"}

    try:
        inventory.quantity -= request.quantity

        total_price = product.price * request.quantity

        sales_order = SalesOrder(
            product_id=request.product_id,
            warehouse_id=request.warehouse_id,
            quantity=request.quantity,
            total_price=total_price,
        )

        saved_order = save(db, sales_order)

        db.commit()
        db.refresh(saved_order)

        return map_sales_order(saved_order)

    except Exception:
        db.rollback()

        return {"message": "Sales order failed"}


def get_all_sales_orders(db: Session):
    sales_orders = find_all(db)

    return [map_sales_order(order) for order in sales_orders]
