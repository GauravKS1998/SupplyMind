from sqlalchemy.orm import Session

from .model import Supplier

from .schema import SupplierCreateRequest, SupplierUpdateRequest, SupplierResponse

from .repository import find_all, find_by_id, save, delete


def get_all_suppliers(db: Session):
    suppliers = find_all(db)

    return [
        SupplierResponse(
            id=supplier.id,
            name=supplier.name,
            contact_email=supplier.contact_email,
            phone=supplier.phone,
            address=supplier.address,
            created_at=supplier.created_at,
        )
        for supplier in suppliers
    ]


def get_supplier_by_id(db: Session, supplier_id: int):
    supplier = find_by_id(db, supplier_id)

    if not supplier:
        return {"message": "Supplier not found"}

    return SupplierResponse(
        id=supplier.id,
        name=supplier.name,
        contact_email=supplier.contact_email,
        phone=supplier.phone,
        address=supplier.address,
        created_at=supplier.created_at,
    )


def create_supplier(db: Session, request: SupplierCreateRequest):
    supplier = Supplier(
        name=request.name,
        contact_email=request.contact_email,
        phone=request.phone,
        address=request.address,
    )

    saved_supplier = save(db, supplier)

    return SupplierResponse(
        id=saved_supplier.id,
        name=saved_supplier.name,
        contact_email=saved_supplier.contact_email,
        phone=saved_supplier.phone,
        address=saved_supplier.address,
        created_at=saved_supplier.created_at,
    )


def update_supplier(db: Session, supplier_id: int, request: SupplierUpdateRequest):
    supplier = find_by_id(db, supplier_id)

    if not supplier:
        return {"message": "Supplier not found"}

    supplier.name = request.name
    supplier.contact_email = request.contact_email
    supplier.phone = request.phone
    supplier.address = request.address

    updated_supplier = save(db, supplier)

    return SupplierResponse(
        id=updated_supplier.id,
        name=updated_supplier.name,
        contact_email=updated_supplier.contact_email,
        phone=updated_supplier.phone,
        address=updated_supplier.address,
        created_at=updated_supplier.created_at,
    )


def delete_supplier(db: Session, supplier_id: int):
    supplier = find_by_id(db, supplier_id)

    if not supplier:
        return {"message": "Supplier not found"}

    delete(db, supplier)

    return {"message": "Supplier deleted successfully"}
