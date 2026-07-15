from sqlalchemy import func
from sqlalchemy.orm import Session

from app.common.filtering import apply_filter
from app.common.search import apply_search
from app.common.sorting import apply_sorting

from .model import Supplier

# -------------------------
# Basic CRUD
# -------------------------


def save(
    db: Session,
    supplier: Supplier,
):
    db.add(supplier)
    db.flush()

    return supplier


def find_by_id(
    db: Session,
    supplier_id: int,
):
    return db.query(Supplier).filter(Supplier.id == supplier_id).first()


def find_by_user_id(
    db: Session,
    user_id: int,
):
    return db.query(Supplier).filter(Supplier.user_id == user_id).first()


def find_by_gst_number(
    db: Session,
    gst_number: str,
):
    return db.query(Supplier).filter(Supplier.gst_number == gst_number).first()


# -------------------------
# Simple Lists
# -------------------------


def find_all(
    db: Session,
):
    return db.query(Supplier).order_by(Supplier.company_name.asc()).all()


def find_all_active(
    db: Session,
):
    return (
        db.query(Supplier)
        .filter(Supplier.is_active.is_(True))
        .order_by(Supplier.company_name.asc())
        .all()
    )


def find_all_inactive(
    db: Session,
):
    return (
        db.query(Supplier)
        .filter(Supplier.is_active.is_(False))
        .order_by(Supplier.company_name.asc())
        .all()
    )


def find_all_pending_verification(
    db: Session,
):
    return (
        db.query(Supplier)
        .filter(Supplier.is_verified.is_(False))
        .order_by(Supplier.created_at.desc())
        .all()
    )


# -------------------------
# Supplier Search
# -------------------------


ALLOWED_SORT_FIELDS = {
    "company_name",
    "gst_number",
    "supplier_type",
    "lead_time_days",
    "rating",
    "created_at",
    "updated_at",
}


def find_suppliers(
    db: Session,
    page: int = 1,
    size: int = 20,
    search: str | None = None,
    supplier_type: str | None = None,
    city: str | None = None,
    state: str | None = None,
    country: str | None = None,
    is_verified: bool | None = None,
    is_active: bool | None = None,
    sort_by: str | None = None,
    direction: str = "asc",
):

    query = db.query(Supplier)

    # -----------------------
    # Filtering
    # -----------------------

    query = apply_filter(
        query,
        Supplier,
        supplier_type=supplier_type,
        city=city,
        state=state,
        country=country,
        is_verified=is_verified,
        is_active=is_active,
    )

    # -----------------------
    # Search
    # -----------------------

    query = apply_search(
        query,
        [
            Supplier.company_name,
            Supplier.gst_number,
            Supplier.contact_person,
            Supplier.phone,
            Supplier.email,
            Supplier.city,
            Supplier.state,
            Supplier.country,
        ],
        search,
    )

    # -----------------------
    # Count Before Pagination
    # -----------------------

    total_items = query.with_entities(func.count(Supplier.id)).scalar()

    # -----------------------
    # Sorting
    # -----------------------

    if sort_by:
        if sort_by not in ALLOWED_SORT_FIELDS:
            sort_by = "created_at"
    else:
        sort_by = "created_at"

    query = apply_sorting(
        query,
        Supplier,
        sort_by,
        direction,
    )

    # -----------------------
    # Pagination
    # -----------------------

    items = query.offset((page - 1) * size).limit(size).all()

    return items, total_items
