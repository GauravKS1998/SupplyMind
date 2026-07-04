from sqlalchemy.orm import Session

from .model import Inventory

from .schema import InventoryCreateRequest, InventoryUpdateRequest, InventoryResponse

from .repository import find_all, find_by_id, save, delete

from app.products.repository import find_by_id as find_product_by_id
from app.warehouses.repository import find_by_id as find_warehouse_by_id


def map_inventory_response(inventory: Inventory):
    return InventoryResponse(
        id=inventory.id,
        product_id=inventory.product_id,
        product_name=inventory.product.name,
        product_sku=inventory.product.sku,
        supplier_name=inventory.product.supplier.name,
        category_name=inventory.product.category.name,
        subcategory_name=inventory.product.subcategory.name,
        product_type_name=inventory.product.product_type.name,
        warehouse_id=inventory.warehouse_id,
        warehouse_name=inventory.warehouse.name,
        quantity=inventory.quantity,
        reorder_level=inventory.reorder_level,
        created_at=inventory.created_at,
    )


def get_all_inventories(db: Session):
    inventories = find_all(db)

    return [map_inventory_response(inventory) for inventory in inventories]


def get_inventory_by_id(db: Session, inventory_id: int):
    inventory = find_by_id(db, inventory_id)

    if not inventory:
        return {"message": "Inventory not found"}

    return map_inventory_response(inventory)


def create_inventory(db: Session, request: InventoryCreateRequest):
    product = find_product_by_id(db, request.product_id)

    if not product:
        return {"message": "Product not found"}

    warehouse = find_warehouse_by_id(db, request.warehouse_id)

    if not warehouse:
        return {"message": "Warehouse not found"}

    inventory = Inventory(
        product_id=request.product_id,
        warehouse_id=request.warehouse_id,
        quantity=request.quantity,
        reorder_level=request.reorder_level,
    )

    saved_inventory = save(db, inventory)

    return map_inventory_response(saved_inventory)


def update_inventory(db: Session, inventory_id: int, request: InventoryUpdateRequest):
    inventory = find_by_id(db, inventory_id)

    if not inventory:
        return {"message": "Inventory not found"}

    inventory.quantity = request.quantity
    inventory.reorder_level = request.reorder_level

    updated_inventory = save(db, inventory)

    return map_inventory_response(updated_inventory)


def delete_inventory(db: Session, inventory_id: int):
    inventory = find_by_id(db, inventory_id)

    if not inventory:
        return {"message": "Inventory not found"}

    delete(db, inventory)

    return {"message": "Inventory deleted successfully"}
