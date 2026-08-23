from sqlalchemy import func
from sqlalchemy.orm import Session

from app.common.filtering import apply_filter
from app.common.search import apply_search
from app.common.sorting import apply_sorting

from .model import Customer

# =========================================================
# Basic CRUD
# =========================================================


def save(
    db: Session,
    customer: Customer,
):
    db.add(customer)
    db.flush()

    return customer


def find_by_id(
    db: Session,
    customer_id: int,
):
    return db.query(Customer).filter(Customer.id == customer_id).first()


def find_by_user_id(
    db: Session,
    user_id: int,
):
    return db.query(Customer).filter(Customer.user_id == user_id).first()


def find_by_gst_number(
    db: Session,
    gst_number: str,
):
    return db.query(Customer).filter(Customer.gst_number == gst_number).first()


# =========================================================
# Lists
# =========================================================


def find_all(
    db: Session,
):
    return db.query(Customer).order_by(Customer.company_name.asc()).all()


def find_all_active(
    db: Session,
):
    return (
        db.query(Customer)
        .filter(Customer.is_active.is_(True))
        .order_by(Customer.company_name.asc())
        .all()
    )


def find_all_inactive(
    db: Session,
):
    return (
        db.query(Customer)
        .filter(Customer.is_active.is_(False))
        .order_by(Customer.company_name.asc())
        .all()
    )


def find_all_pending_verification(
    db: Session,
):
    return (
        db.query(Customer)
        .filter(Customer.is_verified.is_(False))
        .order_by(Customer.created_at.desc())
        .all()
    )


# =========================================================
# Search
# =========================================================


ALLOWED_SORT_FIELDS = {
    "company_name",
    "gst_number",
    "contact_person",
    "city",
    "state",
    "country",
    "is_verified",
    "is_active",
    "created_at",
    "updated_at",
}


def find_customers(
    db: Session,
    page: int = 1,
    size: int = 20,
    search: str | None = None,
    city: str | None = None,
    state: str | None = None,
    country: str | None = None,
    is_verified: bool | None = None,
    is_active: bool | None = None,
    sort_by: str | None = None,
    direction: str = "asc",
):

    query = db.query(Customer)

    # -----------------------------------------
    # Filtering
    # -----------------------------------------

    query = apply_filter(
        query,
        Customer,
        city=city,
        state=state,
        country=country,
        is_verified=is_verified,
        is_active=is_active,
    )

    # -----------------------------------------
    # Search
    # -----------------------------------------

    query = apply_search(
        query,
        [
            Customer.company_name,
            Customer.gst_number,
            Customer.contact_person,
            Customer.phone,
            Customer.email,
            Customer.city,
            Customer.state,
            Customer.country,
        ],
        search,
    )

    # -----------------------------------------
    # Count
    # -----------------------------------------

    total_items = query.with_entities(func.count(Customer.id)).scalar()

    # -----------------------------------------
    # Sorting
    # -----------------------------------------

    if sort_by:
        if sort_by not in ALLOWED_SORT_FIELDS:
            sort_by = "created_at"
    else:
        sort_by = "created_at"

    query = apply_sorting(
        query,
        Customer,
        sort_by,
        direction,
    )

    # -----------------------------------------
    # Pagination
    # -----------------------------------------

    items = query.offset((page - 1) * size).limit(size).all()

    return items, total_items
