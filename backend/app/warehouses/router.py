from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from .schema import WarehouseCreateRequest, WarehouseUpdateRequest

from .service import (
    create_warehouse,
    update_warehouse,
    deactivate_warehouse,
    reactivate_warehouse,
    get_active_warehouses,
    get_inactive_warehouses,
)

router = APIRouter()


@router.post("/")
def create(request: WarehouseCreateRequest, db: Session = Depends(get_db)):
    return create_warehouse(db, request)


@router.put("/{warehouse_id}")
def update(
    warehouse_id: int, request: WarehouseUpdateRequest, db: Session = Depends(get_db)
):
    return update_warehouse(db, warehouse_id, request)


@router.put("/{warehouse_id}/deactivate")
def deactivate(warehouse_id: int, db: Session = Depends(get_db)):
    return deactivate_warehouse(db, warehouse_id)


@router.put("/{warehouse_id}/reactivate")
def reactivate(warehouse_id: int, db: Session = Depends(get_db)):
    return reactivate_warehouse(db, warehouse_id)


@router.get("/active")
def get_active(db: Session = Depends(get_db)):
    return get_active_warehouses(db)


@router.get("/inactive")
def get_inactive(db: Session = Depends(get_db)):
    return get_inactive_warehouses(db)
