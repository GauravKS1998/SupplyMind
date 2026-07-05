from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from .schema import SupplierCreateRequest, SupplierUpdateRequest

from .service import (
    create_supplier,
    update_supplier,
    verify_supplier,
    get_pending_suppliers,
    deactivate_supplier,
    reactivate_supplier,
    get_active_suppliers,
    get_inactive_suppliers,
)

router = APIRouter()


@router.post("/")
def create(request: SupplierCreateRequest, db: Session = Depends(get_db)):
    return create_supplier(db, request)


@router.put("/{supplier_id}")
def update(
    supplier_id: int, request: SupplierUpdateRequest, db: Session = Depends(get_db)
):
    return update_supplier(db, supplier_id, request)


@router.put("/{supplier_id}/verify")
def verify(supplier_id: int, db: Session = Depends(get_db)):
    return verify_supplier(db, supplier_id)


@router.get("/pending")
def get_pending(db: Session = Depends(get_db)):
    return get_pending_suppliers(db)


@router.put("/{supplier_id}/deactivate")
def deactivate(supplier_id: int, db: Session = Depends(get_db)):
    return deactivate_supplier(db, supplier_id)


@router.put("/{supplier_id}/reactivate")
def reactivate(supplier_id: int, db: Session = Depends(get_db)):
    return reactivate_supplier(db, supplier_id)


@router.get("/active")
def get_active(db: Session = Depends(get_db)):
    return get_active_suppliers(db)


@router.get("/inactive")
def get_inactive(db: Session = Depends(get_db)):
    return get_inactive_suppliers(db)
