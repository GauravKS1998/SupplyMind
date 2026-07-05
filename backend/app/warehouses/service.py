from sqlalchemy.orm import Session

from .model import Warehouse

from .schema import WarehouseCreateRequest, WarehouseUpdateRequest, WarehouseResponse

from .repository import (
    save,
    find_by_id,
    find_by_code,
    find_all_active,
    find_all_inactive,
)

from .exceptions import WarehouseNotFoundException, WarehouseAlreadyExistsException


def create_warehouse(db: Session, request: WarehouseCreateRequest):
    existing = find_by_code(db, request.warehouse_code)

    if existing:
        raise WarehouseAlreadyExistsException("Warehouse code already exists")

    warehouse = Warehouse(**request.model_dump())

    saved = save(db, warehouse)

    return WarehouseResponse.model_validate(saved, from_attributes=True)


def update_warehouse(db: Session, warehouse_id: int, request: WarehouseUpdateRequest):
    warehouse = find_by_id(db, warehouse_id)

    if not warehouse:
        raise WarehouseNotFoundException("Warehouse not found")

    for key, value in request.model_dump().items():
        setattr(warehouse, key, value)

    db.commit()
    db.refresh(warehouse)

    return WarehouseResponse.model_validate(warehouse, from_attributes=True)


def deactivate_warehouse(db: Session, warehouse_id: int):
    warehouse = find_by_id(db, warehouse_id)

    if not warehouse:
        raise WarehouseNotFoundException("Warehouse not found")

    warehouse.is_active = False

    db.commit()
    db.refresh(warehouse)

    return {"message": "Warehouse deactivated successfully"}


def reactivate_warehouse(db: Session, warehouse_id: int):
    warehouse = find_by_id(db, warehouse_id)

    if not warehouse:
        raise WarehouseNotFoundException("Warehouse not found")

    warehouse.is_active = True

    db.commit()
    db.refresh(warehouse)

    return {"message": "Warehouse reactivated successfully"}


def get_active_warehouses(db: Session):
    warehouses = find_all_active(db)

    return [
        WarehouseResponse.model_validate(warehouse, from_attributes=True)
        for warehouse in warehouses
    ]


def get_inactive_warehouses(db: Session):
    warehouses = find_all_inactive(db)

    return [
        WarehouseResponse.model_validate(warehouse, from_attributes=True)
        for warehouse in warehouses
    ]
