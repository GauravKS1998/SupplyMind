from sqlalchemy import func
from sqlalchemy.orm import Session

from app.common.filtering import apply_filter
from app.common.search import apply_search
from app.common.sorting import apply_sorting

from .model import Warehouse


def save(db: Session, warehouse: Warehouse):
    db.add(warehouse)
    db.flush()

    return warehouse


def find_by_id(db: Session, warehouse_id: int):
    return db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()


def find_by_code(db: Session, warehouse_code: str):
    return (
        db.query(Warehouse).filter(Warehouse.warehouse_code == warehouse_code).first()
    )


def find_all(db: Session):
    return db.query(Warehouse).order_by(Warehouse.warehouse_type.asc()).all()


def find_all_active(db: Session):
    return (
        db.query(Warehouse)
        .filter(Warehouse.is_active.is_(True))
        .order_by(Warehouse.warehouse_type.asc())
        .all()
    )


def find_all_inactive(db: Session):
    return (
        db.query(Warehouse)
        .filter(Warehouse.is_active.is_(False))
        .order_by(Warehouse.warehouse_type.asc())
        .all()
    )


def find_by_manager_user_id(
    db: Session,
    manager_user_id: int,
):
    return (
        db.query(Warehouse).filter(Warehouse.manager_user_id == manager_user_id).all()
    )


ALLOWED_SORT_FIELDS = {
    "warehouse_code",
    "name",
    "warehouse_type",
    "created_at",
    "updated_at",
}


def find_warehouses(
    db: Session,
    page: int = 1,
    size: int = 20,
    search: str | None = None,
    warehouse_type: str | None = None,
    city: str | None = None,
    state: str | None = None,
    country: str | None = None,
    is_active: bool | None = None,
    sort_by: str | None = None,
    direction: str = "asc",
):
    query = db.query(Warehouse)

    # -----------------------
    # Filtering
    # -----------------------

    query = apply_filter(
        query,
        Warehouse,
        warehouse_type=warehouse_type,
        city=city,
        state=state,
        country=country,
        is_active=is_active,
    )

    # -----------------------
    # Search
    # -----------------------

    query = apply_search(
        query,
        [
            Warehouse.name,
            Warehouse.warehouse_code,
            Warehouse.city,
            Warehouse.state,
            Warehouse.country,
        ],
        search,
    )

    # -----------------------
    # Count Before Pagination
    # -----------------------

    total_items = query.with_entities(func.count(Warehouse.id)).scalar()

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
        Warehouse,
        sort_by,
        direction,
    )

    # -----------------------
    # Pagination
    # -----------------------

    items = query.offset((page - 1) * size).limit(size).all()

    return items, total_items
