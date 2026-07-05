from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from .service import (
    get_all_inventories,
    get_inventory_by_id,
    create_inventory,
    update_inventory,
    deactivate_inventory,
    reactivate_inventory,
)

from .schema import InventoryCreateRequest, InventoryUpdateRequest

router = APIRouter()


@router.get("/")
def get_inventories(db: Session = Depends(get_db)):
    return get_all_inventories(db)


@router.get("/{inventory_id}")
def get_single_inventory(inventory_id: int, db: Session = Depends(get_db)):
    return get_inventory_by_id(db, inventory_id)


@router.post("/")
def add_inventory(request: InventoryCreateRequest, db: Session = Depends(get_db)):
    return create_inventory(db, request)


@router.put("/{inventory_id}")
def update(
    inventory_id: int, request: InventoryUpdateRequest, db: Session = Depends(get_db)
):
    return update_inventory(db, inventory_id, request)


@router.put("/{inventory_id}/deactivate")
def deactivate(inventory_id: int, db: Session = Depends(get_db)):
    return deactivate_inventory(db, inventory_id)


@router.put("/{inventory_id}/reactivate")
def reactivate(inventory_id: int, db: Session = Depends(get_db)):
    return reactivate_inventory(db, inventory_id)
