from sqlalchemy.orm import Session

from .model import Inventory

from .schema import InventoryCreateRequest, InventoryUpdateRequest, InventoryResponse

from .repository import find_all, find_by_id, save, delete

from app.products.repository import find_by_id as find_product_by_id
from app.warehouses.repository import find_by_id as find_warehouse_by_id

from .exceptions import InventoryNotFoundException, InventoryAlreadyExistsException


def map_inventory_response(inventory):
    return InventoryResponse(
        id=inventory.id,
        product_id=inventory.product.id,
        product_name=inventory.product.name,
        product_sku=inventory.product.sku,
        supplier_name=inventory.product.supplier.company_name,
        category_name=inventory.product.category.name,
        subcategory_name=inventory.product.subcategory.name,
        product_type_name=inventory.product.product_type.name,
        warehouse_id=inventory.warehouse.id,
        warehouse_name=inventory.warehouse.name,
        quantity=inventory.quantity,
        reserved_quantity=inventory.reserved_quantity,
        available_quantity=inventory.available_quantity,
        reorder_level=inventory.reorder_level,
        reorder_quantity=inventory.reorder_quantity,
        batch_number=inventory.batch_number,
        expiry_date=inventory.expiry_date,
        last_stocked_at=inventory.last_stocked_at,
    )


def get_all_inventories(db: Session):
    inventories = find_all(db)

    return [map_inventory_response(inventory) for inventory in inventories]


def get_inventory_by_id(db: Session, inventory_id: int):
    inventory = find_by_id(db, inventory_id)

    if not inventory:
        raise InventoryNotFoundException("Inventory not found")

    return map_inventory_response(inventory)


def create_inventory(db: Session, request: InventoryCreateRequest):
    inventory = Inventory(
        product_id=request.product_id,
        warehouse_id=request.warehouse_id,
        quantity=request.quantity,
        reserved_quantity=0,
        available_quantity=request.quantity,
        reorder_level=request.reorder_level,
        reorder_quantity=request.reorder_quantity,
        batch_number=request.batch_number,
        expiry_date=request.expiry_date,
    )

    saved_inventory = save(db, inventory)

    return map_inventory_response(saved_inventory)


def update_inventory(db: Session, inventory_id: int, request: InventoryUpdateRequest):
    inventory = find_by_id(db, inventory_id)

    if not inventory:
        raise InventoryNotFoundException("Inventory not found")

    inventory.quantity = request.quantity
    inventory.reserved_quantity = request.reserved_quantity

    inventory.available_quantity = request.quantity - request.reserved_quantity

    inventory.reorder_level = request.reorder_level
    inventory.reorder_quantity = request.reorder_quantity
    inventory.batch_number = request.batch_number
    inventory.expiry_date = request.expiry_date

    db.commit()
    db.refresh(inventory)

    return map_inventory_response(inventory)


def deactivate_inventory(db: Session, inventory_id: int):
    inventory = find_by_id(db, inventory_id)

    if not inventory:
        raise InventoryNotFoundException("Inventory not found")

    inventory.is_active = False

    db.commit()
    db.refresh(inventory)

    return {"message": "Inventory deactivated successfully"}


def reactivate_inventory(db: Session, inventory_id: int):
    inventory = find_by_id(db, inventory_id)

    if not inventory:
        raise InventoryNotFoundException("Inventory not found")

    inventory.is_active = True

    db.commit()
    db.refresh(inventory)

    return {"message": "Inventory reactivated successfully"}
