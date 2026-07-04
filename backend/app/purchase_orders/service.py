from sqlalchemy.orm import Session

from .model import PurchaseOrder
from .schema import PurchaseOrderCreateRequest, PurchaseOrderResponse

from .repository import find_all, find_by_id, save

from app.suppliers.repository import find_by_id as find_supplier_by_id

from app.products.repository import find_by_id as find_product_by_id

from app.warehouses.repository import find_by_id as find_warehouse_by_id

from app.inventories.repository import (
    find_by_product_and_warehouse,
    save as save_inventory,
)

from app.inventories.model import Inventory


def map_purchase_order(purchase_order: PurchaseOrder):
    return PurchaseOrderResponse(
        id=purchase_order.id,
        supplier_id=purchase_order.supplier_id,
        supplier_name=purchase_order.supplier.name,
        product_id=purchase_order.product_id,
        product_name=purchase_order.product.name,
        product_sku=purchase_order.product.sku,
        warehouse_id=purchase_order.warehouse_id,
        warehouse_name=purchase_order.warehouse.name,
        quantity=purchase_order.quantity,
        status=purchase_order.status,
        ordered_at=purchase_order.ordered_at,
    )


def get_all_purchase_orders(db: Session):
    purchase_orders = find_all(db)

    return [map_purchase_order(po) for po in purchase_orders]


def create_purchase_order(db: Session, request: PurchaseOrderCreateRequest):
    supplier = find_supplier_by_id(db, request.supplier_id)

    if not supplier:
        return {"message": "Supplier not found"}

    product = find_product_by_id(db, request.product_id)

    if not product:
        return {"message": "Product not found"}

    warehouse = find_warehouse_by_id(db, request.warehouse_id)

    if not warehouse:
        return {"message": "Warehouse not found"}

    purchase_order = PurchaseOrder(
        supplier_id=request.supplier_id,
        product_id=request.product_id,
        warehouse_id=request.warehouse_id,
        quantity=request.quantity,
    )

    saved_po = save(db, purchase_order)

    return map_purchase_order(saved_po)


def approve_purchase_order(db: Session, purchase_order_id: int):
    purchase_order = find_by_id(db, purchase_order_id)

    if not purchase_order:
        return {"message": "Purchase order not found"}

    if purchase_order.status != "PENDING":
        return {"message": "Purchase order has already been processed"}

    inventory = find_by_product_and_warehouse(
        db, purchase_order.product_id, purchase_order.warehouse_id
    )

    if inventory:
        inventory.quantity += purchase_order.quantity
    else:
        inventory = Inventory(
            product_id=purchase_order.product_id,
            warehouse_id=purchase_order.warehouse_id,
            quantity=purchase_order.quantity,
            reorder_level=10,
        )

    save_inventory(db, inventory)

    purchase_order.status = "COMPLETED"

    saved_po = save(db, purchase_order)

    return map_purchase_order(saved_po)
