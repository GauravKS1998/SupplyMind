from sqlalchemy import func
from sqlalchemy.orm import Session

from app.common.filtering import apply_filter
from app.common.search import apply_search
from app.common.sorting import apply_sorting

from .model import UnitOfMeasure


def save(
    db: Session,
    uom: UnitOfMeasure,
):
    db.add(uom)
    db.flush()

    return uom


def find_by_id(
    db: Session,
    uom_id: int,
):
    return db.query(UnitOfMeasure).filter(UnitOfMeasure.id == uom_id).first()


def find_by_name(
    db: Session,
    name: str,
):
    return (
        db.query(UnitOfMeasure)
        .filter(func.lower(UnitOfMeasure.name) == name.strip().lower())
        .first()
    )


def find_by_code(
    db: Session,
    code: str,
):
    return (
        db.query(UnitOfMeasure)
        .filter(func.lower(UnitOfMeasure.code) == code.strip().lower())
        .first()
    )


ALLOWED_SORT_FIELDS = {
    "name",
    "code",
    "created_at",
    "updated_at",
}


def find_units_of_measure(
    db: Session,
    page: int = 1,
    size: int = 20,
    search: str | None = None,
    is_active: bool | None = None,
    sort_by: str | None = None,
    direction: str = "asc",
):
    query = db.query(UnitOfMeasure)

    query = apply_filter(
        query,
        UnitOfMeasure,
        is_active=is_active,
    )

    query = apply_search(
        query,
        [
            UnitOfMeasure.name,
            UnitOfMeasure.code,
        ],
        search,
    )

    # Count how many units of measure exist after filter & search
    total_items = query.with_entities(func.count(UnitOfMeasure.id)).scalar()

    if not sort_by or sort_by not in ALLOWED_SORT_FIELDS:
        sort_by = "created_at"

    query = apply_sorting(
        query,
        UnitOfMeasure,
        sort_by,
        direction,
    )

    items = query.offset((page - 1) * size).limit(size).all()

    return items, total_items
