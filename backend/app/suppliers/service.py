from datetime import datetime, timezone

from sqlalchemy.orm import Session

from .model import Supplier

from .schema import SupplierCreateRequest, SupplierUpdateRequest, SupplierResponse

from .repository import (
    save,
    find_by_id,
    find_by_user_id,
    find_all_pending_verification,
    find_all_active,
    find_all_inactive,
)

from .exceptions import SupplierNotFoundException, UnauthorizedAccessException


def create_supplier(db: Session, request: SupplierCreateRequest):
    supplier = Supplier(**request.model_dump())

    saved_supplier = save(db, supplier)

    return SupplierResponse.model_validate(saved_supplier, from_attributes=True)


def update_supplier(
    db: Session, supplier_id: int, request: SupplierUpdateRequest, current_user_id: int
):
    supplier = find_by_id(db, supplier_id)

    if not supplier:
        raise SupplierNotFoundException("Supplier not found")

    if supplier.user_id != current_user_id:
        raise UnauthorizedAccessException("Unauthorized access")

    for key, value in request.model_dump().items():
        setattr(supplier, key, value)

    supplier.updated_by = current_user_id
    supplier.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(supplier)

    return SupplierResponse.model_validate(supplier, from_attributes=True)


def verify_supplier(db: Session, supplier_id: int, current_user_id: int):
    supplier = find_by_id(db, supplier_id)

    if not supplier:
        raise SupplierNotFoundException("Supplier not found")

    supplier.is_verified = True
    supplier.verified_by = current_user_id

    db.commit()
    db.refresh(supplier)

    return {"message": "Supplier verified"}


def get_pending_suppliers(db: Session):
    suppliers = find_all_pending_verification(db)

    return [
        SupplierResponse.model_validate(supplier, from_attributes=True)
        for supplier in suppliers
    ]


def deactivate_supplier(db: Session, supplier_id: int, current_user_id: int):
    supplier = find_by_id(db, supplier_id)

    if not supplier:
        raise SupplierNotFoundException("Supplier not found")

    supplier.is_active = False
    supplier.deactivated_by = current_user_id

    db.commit()
    db.refresh(supplier)

    return {"message": "Supplier deactivated successfully"}


def reactivate_supplier(db: Session, supplier_id: int, current_user_id: int):
    supplier = find_by_id(db, supplier_id)

    if not supplier:
        raise SupplierNotFoundException("Supplier not found")

    supplier.is_active = True
    supplier.reactivated_by = current_user_id

    db.commit()
    db.refresh(supplier)

    return {"message": "Supplier reactivated successfully"}


def get_active_suppliers(db: Session):
    suppliers = find_all_active(db)

    return [
        SupplierResponse.model_validate(supplier, from_attributes=True)
        for supplier in suppliers
    ]


def get_inactive_suppliers(db: Session):
    suppliers = find_all_inactive(db)

    return [
        SupplierResponse.model_validate(supplier, from_attributes=True)
        for supplier in suppliers
    ]
