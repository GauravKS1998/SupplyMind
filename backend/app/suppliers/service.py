from datetime import datetime, timezone
from math import ceil

from sqlalchemy.orm import Session

from app.common.responses import PaginatedResponse
from app.common.pagination import PaginationMeta
from app.common.entity_utils import get_or_raise

from app.logging.logger import logger

from .model import Supplier

from .schema import (
    SupplierCreateRequest,
    SupplierUpdateRequest,
    SupplierSearchRequest,
)

from .repository import (
    save,
    find_by_id,
    find_by_user_id,
    find_by_gst_number,
    find_all,
    find_all_pending_verification,
    find_all_active,
    find_all_inactive,
    find_suppliers,
)

from .mapper import (
    map_supplier,
    map_suppliers,
)

from .exceptions import (
    SupplierNotFoundException,
    SupplierAlreadyExistsException,
    SupplierAccessDeniedException,
)

# -------------------------
# Get Supplier
# -------------------------


def get_supplier_by_id(
    db: Session,
    supplier_id: int,
):
    supplier = get_or_raise(
        find_by_id(
            db,
            supplier_id,
        ),
        SupplierNotFoundException("Supplier not found"),
    )

    return map_supplier(supplier)


def get_supplier_by_user_id(
    db: Session,
    user_id: int,
):
    supplier = get_or_raise(
        find_by_user_id(
            db,
            user_id,
        ),
        SupplierNotFoundException("Supplier not found"),
    )

    return map_supplier(supplier)


# -------------------------
# Simple Lists
# -------------------------


def get_all_suppliers(
    db: Session,
):
    suppliers = find_all(db)

    return map_suppliers(suppliers)


def get_active_suppliers(
    db: Session,
):
    suppliers = find_all_active(db)

    return map_suppliers(suppliers)


def get_inactive_suppliers(
    db: Session,
):
    suppliers = find_all_inactive(db)

    return map_suppliers(suppliers)


def get_pending_suppliers(
    db: Session,
):
    suppliers = find_all_pending_verification(db)

    return map_suppliers(suppliers)


# -------------------------
# Search
# -------------------------


def search_suppliers(
    db: Session,
    request: SupplierSearchRequest,
):
    suppliers, total_items = find_suppliers(
        db=db,
        page=request.page,
        size=request.size,
        search=request.search,
        supplier_type=request.supplier_type,
        city=request.city,
        state=request.state,
        country=request.country,
        is_verified=request.is_verified,
        is_active=request.is_active,
        sort_by=request.sort_by,
        direction=request.direction,
    )

    total_pages = ceil(total_items / request.size) if total_items > 0 else 0

    return PaginatedResponse(
        items=map_suppliers(suppliers),
        pagination=PaginationMeta(
            page=request.page,
            size=request.size,
            total_items=total_items,
            total_pages=total_pages,
            has_next=(request.page < total_pages),
            has_previous=(request.page > 1),
        ),
    )


# -------------------------
# Create
# -------------------------


def create_supplier(
    db: Session,
    request: SupplierCreateRequest,
    current_user_id: int,
):
    existing_user_supplier = find_by_user_id(
        db,
        request.user_id,
    )

    if existing_user_supplier:
        raise SupplierAlreadyExistsException(
            "Supplier profile already exists for this user"
        )

    existing_gst = find_by_gst_number(
        db,
        request.gst_number,
    )

    if existing_gst:
        raise SupplierAlreadyExistsException(
            "Supplier with this GST number already exists"
        )

    supplier = Supplier(user_id=current_user_id, **request.model_dump())

    saved_supplier = save(
        db,
        supplier,
    )

    db.commit()
    db.refresh(saved_supplier)

    logger.info(f"Supplier {saved_supplier.id} created")

    return map_supplier(saved_supplier)


# -------------------------
# Update
# -------------------------


def update_supplier(
    db: Session,
    supplier_id: int,
    request: SupplierUpdateRequest,
    current_user_id: int,
):
    supplier = get_or_raise(
        find_by_id(
            db,
            supplier_id,
        ),
        SupplierNotFoundException("Supplier not found"),
    )

    if supplier.user_id != current_user_id:
        raise SupplierAccessDeniedException(
            "You are not authorized to update this supplier"
        )

    existing_gst = find_by_gst_number(
        db,
        request.gst_number,
    )

    if existing_gst and existing_gst.id != supplier.id:
        raise SupplierAlreadyExistsException(
            "Supplier with this GST number already exists"
        )

    for key, value in request.model_dump().items():
        setattr(
            supplier,
            key,
            value,
        )

    supplier.updated_by = current_user_id
    supplier.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(supplier)

    logger.info(f"Supplier {supplier.id} updated")

    return map_supplier(supplier)


# -------------------------
# Verification
# -------------------------


def verify_supplier(
    db: Session,
    supplier_id: int,
    current_user_id: int,
):
    supplier = get_or_raise(
        find_by_id(
            db,
            supplier_id,
        ),
        SupplierNotFoundException("Supplier not found"),
    )

    if supplier.is_verified:
        return {"message": "Supplier already verified"}

    supplier.is_verified = True
    supplier.verified_by = current_user_id
    supplier.updated_by = current_user_id
    supplier.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(supplier)

    logger.info(f"Supplier {supplier.id} verified")

    return {"message": "Supplier verified successfully"}


# -------------------------
# Deactivate
# -------------------------


def deactivate_supplier(
    db: Session,
    supplier_id: int,
    current_user_id: int,
):
    supplier = get_or_raise(
        find_by_id(
            db,
            supplier_id,
        ),
        SupplierNotFoundException("Supplier not found"),
    )

    if not supplier.is_active:
        return {"message": "Supplier already inactive"}

    supplier.is_active = False

    supplier.deactivated_by = current_user_id

    supplier.updated_by = current_user_id

    supplier.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(supplier)

    logger.info(f"Supplier {supplier.id} deactivated")

    return {"message": "Supplier deactivated successfully"}


# -------------------------
# Reactivate
# -------------------------


def reactivate_supplier(
    db: Session,
    supplier_id: int,
    current_user_id: int,
):
    supplier = get_or_raise(
        find_by_id(
            db,
            supplier_id,
        ),
        SupplierNotFoundException("Supplier not found"),
    )

    if supplier.is_active:
        return {"message": "Supplier already active"}

    supplier.is_active = True

    supplier.reactivated_by = current_user_id

    supplier.updated_by = current_user_id

    supplier.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(supplier)

    logger.info(f"Supplier {supplier.id} reactivated")

    return {"message": "Supplier reactivated successfully"}
