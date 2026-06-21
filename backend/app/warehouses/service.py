from sqlalchemy.orm import Session

from .model import Warehouse

from .schema import WarehouseCreateRequest, WarehouseUpdateRequest, WarehouseResponse

from .repository import find_all, find_by_id, save, delete


def get_all_warehouses(db: Session):
    warehouses = find_all(db)

    return [
        WarehouseResponse(
            id=warehouse.id,
            name=warehouse.name,
            location=warehouse.location,
            capacity=warehouse.capacity,
            created_at=warehouse.created_at,
        )
        for warehouse in warehouses
    ]


def get_warehouse_by_id(db: Session, warehouse_id: int):
    warehouse = find_by_id(db, warehouse_id)

    if not warehouse:
        return {"message": "Warehouse not found"}

    return WarehouseResponse(
        id=warehouse.id,
        name=warehouse.name,
        location=warehouse.location,
        capacity=warehouse.capacity,
        created_at=warehouse.created_at,
    )


def create_warehouse(db: Session, request: WarehouseCreateRequest):
    warehouse = Warehouse(
        name=request.name, location=request.location, capacity=request.capacity
    )

    saved_warehouse = save(db, warehouse)

    return WarehouseResponse(
        id=saved_warehouse.id,
        name=saved_warehouse.name,
        location=saved_warehouse.location,
        capacity=saved_warehouse.capacity,
        created_at=saved_warehouse.created_at,
    )


def update_warehouse(db: Session, warehouse_id: int, request: WarehouseUpdateRequest):
    warehouse = find_by_id(db, warehouse_id)

    if not warehouse:
        return {"message": "Warehouse not found"}

    warehouse.name = request.name
    warehouse.location = request.location
    warehouse.capacity = request.capacity

    updated_warehouse = save(db, warehouse)

    return WarehouseResponse(
        id=updated_warehouse.id,
        name=updated_warehouse.name,
        location=updated_warehouse.location,
        capacity=updated_warehouse.capacity,
        created_at=updated_warehouse.created_at,
    )


def delete_warehouse(db: Session, warehouse_id: int):
    warehouse = find_by_id(db, warehouse_id)

    if not warehouse:
        return {"message": "Warehouse not found"}

    delete(db, warehouse)

    return {"message": "Warehouse deleted successfully"}
