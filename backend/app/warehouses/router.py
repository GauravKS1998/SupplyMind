from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from .service import (
    get_all_warehouses,
    get_warehouse_by_id,
    create_warehouse,
    update_warehouse,
    delete_warehouse,
)

from .schema import WarehouseCreateRequest, WarehouseUpdateRequest, WarehouseResponse

router = APIRouter()


@router.get("/")
def get_warehouse(db: Session = Depends(get_db)):
    return get_all_warehouses(db)


@router.get("/{warehouse_id}")
def get_single_warehouse(db: Session = Depends(get_db), warehouse_id=int):
    return get_warehouse_by_id(db, warehouse_id)


@router.post("/")
def add_warehouse(request: WarehouseCreateRequest, db: Session = Depends(get_db)):
    return create_warehouse(db, request)


@router.put("/{warehouse_id}")
def update_existing_warehouse(
    request: WarehouseUpdateRequest, warehouse_id=int, db: Session = Depends(get_db)
):
    return update_warehouse(db, warehouse_id, request)


@router.delete("/{warehouse_id}")
def remove_warehouse(warehouse_id=int, db: Session = Depends(get_db)):
    return delete_warehouse(db, warehouse_id)
