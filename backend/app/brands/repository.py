from sqlalchemy import func
from sqlalchemy.orm import Session

from app.common.filtering import apply_filter
from app.common.search import apply_search
from app.common.sorting import apply_sorting

from .model import Brand


def save(db: Session, brand: Brand):
    db.add(brand)
    db.flush()

    return brand


def find_by_id(
    db: Session,
    brand_id: int,
):
    return db.query(Brand).filter(Brand.id == brand_id).first()


def find_by_name(
    db: Session,
    name: str,
):
    return (
        db.query(Brand).filter(func.lower(Brand.name) == name.strip().lower()).first()
    )


ALLOWED_SORT_FIELDS = {
    "name",
    "created_at",
    "updated_at",
}


def find_brands(
    db: Session,
    page: int = 1,
    size: int = 20,
    search: str | None = None,
    is_active: bool | None = None,
    sort_by: str | None = None,
    direction: str = "asc",
):
    query = db.query(Brand)

    # Filtering
    query = apply_filter(
        query,
        Brand,
        is_active=is_active,
    )

    # Search
    query = apply_search(
        query,
        [
            Brand.name,
            Brand.description,
        ],
        search,
    )

    # Count after filtering/search, before pagination
    total_items = query.with_entities(func.count(Brand.id)).scalar()

    # Safe sorting
    if not sort_by or sort_by not in ALLOWED_SORT_FIELDS:
        sort_by = "created_at"

    query = apply_sorting(
        query,
        Brand,
        sort_by,
        direction,
    )

    # Pagination
    items = query.offset((page - 1) * size).limit(size).all()

    return items, total_items
