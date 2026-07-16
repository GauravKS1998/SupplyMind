from .model import Warehouse
from .schema import WarehouseResponse


def map_warehouse(warehouse: Warehouse) -> WarehouseResponse:
    return WarehouseResponse(
        id=warehouse.id,
        warehouse_code=warehouse.warehouse_code,
        name=warehouse.name,
        description=warehouse.description,
        warehouse_type=warehouse.warehouse_type,
        manager_user_id=warehouse.manager_user_id,
        capacity=warehouse.capacity,
        current_utilization=warehouse.current_utilization,
        address=warehouse.address,
        city=warehouse.city,
        state=warehouse.state,
        country=warehouse.country,
        postal_code=warehouse.postal_code,
        is_active=warehouse.is_active,
        created_by=warehouse.created_by,
        updated_by=warehouse.updated_by,
        deactivated_by=warehouse.deactivated_by,
        reactivated_by=warehouse.reactivated_by,
        created_at=warehouse.created_at,
        updated_at=warehouse.updated_at,
    )


def map_warehouses(warehouses: list[Warehouse]) -> list[WarehouseResponse]:
    return [map_warehouse(warehouse) for warehouse in warehouses]
