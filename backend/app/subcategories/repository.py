from sqlalchemy import func
from sqlalchemy.orm import Session

from app.common.filtering import apply_filter
from app.common.search import apply_search
from app.common.sorting import apply_sorting

from .model import SubCategory


def find_all(db: Session):
    return db.query(SubCategory).all()


def find_by_id(db: Session, subcategory_id: int):
    return db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()


def find_by_category_id(
    db: Session,
    category_id: int,
):
    return (
        db.query(SubCategory)
        .filter(
            SubCategory.category_id == category_id,
        )
        .order_by(SubCategory.name.asc())
        .all()
    )


def find_active_by_category_id(
    db: Session,
    category_id: int,
):
    return (
        db.query(SubCategory)
        .filter(
            SubCategory.category_id == category_id,
            SubCategory.is_active.is_(True),
        )
        .order_by(SubCategory.name.asc())
        .all()
    )


def find_by_name(db: Session, name: str):
    return db.query(SubCategory).filter(SubCategory.name == name).first()


def find_active(db: Session):
    return db.query(SubCategory).filter(SubCategory.is_active == True).all()


def find_inactive(db: Session):
    return db.query(SubCategory).filter(SubCategory.is_active == False).all()


def save(db: Session, subcategory: SubCategory):
    db.add(subcategory)
    db.flush()

    return subcategory


ALLOWED_SORT_FIELDS = {
    "name",
    "created_at",
    "updated_at",
}


def find_subcategories(
    db: Session,
    page: int = 1,
    size: int = 20,
    search: str | None = None,
    category_id: int | None = None,
    is_active: bool | None = None,
    sort_by: str | None = None,
    direction: str = "asc",
):
    query = db.query(SubCategory)

    # -------------------------
    # Filtering
    # -------------------------

    query = apply_filter(
        query,
        SubCategory,
        category_id=category_id,
        is_active=is_active,
    )

    # -------------------------
    # Search
    # -------------------------

    query = apply_search(
        query,
        [
            SubCategory.name,
        ],
        search,
    )

    # -------------------------
    # Count
    # -------------------------

    total_items = query.with_entities(func.count(SubCategory.id)).scalar()

    # -------------------------
    # Safe sorting
    # -------------------------

    if not sort_by or sort_by not in ALLOWED_SORT_FIELDS:
        sort_by = "created_at"

    query = apply_sorting(
        query,
        SubCategory,
        sort_by,
        direction,
    )

    # -------------------------
    # Pagination
    # -------------------------

    items = query.offset((page - 1) * size).limit(size).all()

    return items, total_items
