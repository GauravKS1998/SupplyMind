from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from .service import (
    get_all_suppliers,
    get_supplier_by_id,
    create_supplier,
    update_supplier,
    delete_supplier,
)

from .schema import SupplierCreateRequest, SupplierUpdateRequest

router = APIRouter()


@router.get("/")
def get_suppliers(db: Session = Depends(get_db)):
    return get_all_suppliers(db)


@router.get("/{supplier_id}")
def get_single_supplier(supplier_id: int, db: Session = Depends(get_db)):
    return get_supplier_by_id(db, supplier_id)


@router.post("/")
def add_supplier(request: SupplierCreateRequest, db: Session = Depends(get_db)):
    return create_supplier(db, request)


@router.put("/{supplier_id}")
def update_existing_supplier(
    supplier_id: int, request: SupplierUpdateRequest, db: Session = Depends(get_db)
):
    return update_supplier(db, supplier_id, request)


@router.delete("/{supplier_id}")
def remove_supplier(supplier_id: int, db: Session = Depends(get_db)):
    return delete_supplier(db, supplier_id)
