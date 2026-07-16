from math import ceil
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.common.responses import PaginatedResponse
from app.common.pagination import PaginationMeta
from app.common.entity_utils import get_or_raise

from app.logging.logger import logger

from .model import Warehouse

from .schema import (
    WarehouseCreateRequest,
    WarehouseUpdateRequest,
    WarehouseSearchRequest,
)

from .repository import (
    save,
    find_by_id,
    find_by_code,
    find_all,
    find_all_active,
    find_all_inactive,
    find_by_manager_user_id,
    find_warehouses,
)

from .mapper import map_warehouse, map_warehouses

from .exceptions import (
    WarehouseNotFoundException,
    WarehouseAlreadyExistsException,
)

from .validators import validate_capacity


def search_warehouses(db: Session, request: WarehouseSearchRequest):
    warehouses, total_items = find_warehouses(
        db=db,
        page=request.page,
        size=request.size,
        search=request.search,
        warehouse_type=request.warehouse_type,
        city=request.city,
        state=request.state,
        country=request.country,
        is_active=request.is_active,
        sort_by=request.sort_by,
        direction=request.direction,
    )

    total_pages = ceil(total_items / request.size) if total_items > 0 else 0

    return PaginatedResponse(
        items=map_warehouses(warehouses),
        pagination=PaginationMeta(
            page=request.page,
            size=request.size,
            total_items=total_items,
            total_pages=total_pages,
            has_next=(request.page < total_pages),
            has_previous=(request.page > 1),
        ),
    )


def get_all_warehouses(db: Session):
    warehouses = find_all(db)

    return map_warehouses(warehouses)


def get_warehouse_by_id(
    db: Session,
    warehouse_id: int,
):
    warehouse = get_or_raise(
        find_by_id(db, warehouse_id), WarehouseNotFoundException("Warehouse not found")
    )

    return map_warehouse(warehouse)


def create_warehouse(
    db: Session, request: WarehouseCreateRequest, current_user_id: int
):
    existing_code = find_by_code(db, request.warehouse_code)

    if existing_code:
        raise WarehouseAlreadyExistsException("Warehouse code already exists")

    validate_capacity(request.capacity)

    warehouse = Warehouse(
        **request.model_dump(),
        created_by=current_user_id,
    )

    saved_warehouse = save(db, warehouse)

    db.commit()
    db.refresh(saved_warehouse)

    logger.info(f"Warehouse {saved_warehouse.id} created")

    return map_warehouse(saved_warehouse)


def update_warehouse(
    db: Session,
    warehouse_id: int,
    request: WarehouseUpdateRequest,
    current_user_id: int,
):
    warehouse = get_or_raise(
        find_by_id(db, warehouse_id), WarehouseNotFoundException("Warehouse not found")
    )

    validate_capacity(request.capacity)

    for key, value in request.model_dump().items():
        setattr(warehouse, key, value)

    warehouse.updated_by = current_user_id
    warehouse.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(warehouse)

    logger.info(f"Warehouse {warehouse.id} updated")

    return map_warehouse(warehouse)


def deactivate_warehouse(db: Session, warehouse_id: int, current_user_id: int):

    warehouse = get_or_raise(
        find_by_id(db, warehouse_id), WarehouseNotFoundException("Warehouse not found")
    )

    if not warehouse.is_active:
        return {"message": "Warehouse already inactive"}

    warehouse.is_active = False
    warehouse.deactivated_by = current_user_id
    warehouse.updated_by = current_user_id
    warehouse.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(warehouse)

    logger.info(f"Warehouse {warehouse.id} deactivated")

    return {"message": "Warehouse deactivated successfully"}


def reactivate_warehouse(db: Session, warehouse_id: int, current_user_id: int):

    warehouse = get_or_raise(
        find_by_id(db, warehouse_id), WarehouseNotFoundException("Warehouse not found")
    )

    if warehouse.is_active:
        return {"message": "Warehouse already active"}

    warehouse.is_active = True
    warehouse.reactivated_by = current_user_id

    warehouse.updated_by = current_user_id
    warehouse.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(warehouse)

    logger.info(f"Warehouse {warehouse.id} reactivated")

    return {"message": "Warehouse reactivated successfully"}


def get_active_warehouses(db: Session):
    warehouses = find_all_active(db)

    return map_warehouses(warehouses)


def get_inactive_warehouses(db: Session):
    warehouses = find_all_inactive(db)

    return map_warehouses(warehouses)
