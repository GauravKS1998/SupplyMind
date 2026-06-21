from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from .service import (
    get_all_inventories,
    get_inventory_by_id,
    create_inventory,
    update_inventory,
    delete_inventory,
)

from .schema import InventoryCreateRequest, InventoryUpdateRequest

router = APIRouter()


@router.get("/")
def get_inventories(db: Session = Depends(get_db)):
    return get_all_inventories(db)


@router.get("/{inventory_id}")
def get_inventories(inventory_id: int, db: Session = Depends(get_db)):
    return get_inventory_by_id(db, inventory_id)


@router.post("/")
def add_inventory(request: InventoryCreateRequest, db: Session = Depends(get_db)):
    return create_inventory(db, request)


@router.put("/{inventory_id}")
def update_existing_inventory(
    inventory_id: int, request: InventoryUpdateRequest, db: Session = Depends(get_db)
):
    return update_inventory(db, inventory_id, request)


@router.delete("/{inventory_id}")
def remove_inventory(inventory_id: int, db: Session = Depends(get_db)):
    return delete_inventory(db, inventory_id)
