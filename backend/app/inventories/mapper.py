from .model import Inventory
from .schema import InventoryResponse


def map_inventory(inventory: Inventory) -> InventoryResponse:
    return InventoryResponse(
        id=inventory.id,
        product_id=inventory.product.id,
        product_name=inventory.product.name,
        product_sku=inventory.product.sku,
        supplier_id=inventory.product.supplier.id,
        supplier_name=inventory.product.supplier.company_name,
        category_id=inventory.product.category.id,
        category_name=inventory.product.category.name,
        subcategory_id=inventory.product.subcategory.id,
        subcategory_name=inventory.product.subcategory.name,
        product_type_id=inventory.product.product_type.id,
        product_type_name=inventory.product.product_type.name,
        warehouse_id=inventory.warehouse.id,
        warehouse_code=inventory.warehouse.warehouse_code,
        warehouse_name=inventory.warehouse.name,
        quantity=inventory.quantity,
        reserved_quantity=inventory.reserved_quantity,
        available_quantity=inventory.available_quantity,
        unit_cost=inventory.unit_cost,
        reorder_level=inventory.reorder_level,
        reorder_quantity=inventory.reorder_quantity,
        batch_number=inventory.batch_number,
        manufacturing_date=inventory.manufacturing_date,
        expiry_date=inventory.expiry_date,
        storage_location=inventory.storage_location,
        last_movement_at=inventory.last_movement_at,
        is_active=inventory.is_active,
        created_by=inventory.created_by,
        updated_by=inventory.updated_by,
        deactivated_by=inventory.deactivated_by,
        reactivated_by=inventory.reactivated_by,
        created_at=inventory.created_at,
        updated_at=inventory.updated_at,
    )


def map_inventories(
    inventories: list[Inventory],
) -> list[InventoryResponse]:
    return [map_inventory(inventory) for inventory in inventories]
