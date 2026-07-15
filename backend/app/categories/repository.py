from sqlalchemy import func
from sqlalchemy.orm import Session

from app.common.filtering import apply_filter
from app.common.search import apply_search
from app.common.sorting import apply_sorting

from .model import Category


def find_all(db: Session):
    return db.query(Category).all()


def find_by_id(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()


def find_by_name(db: Session, name: str):
    return db.query(Category).filter(Category.name == name).first()


def find_active(db: Session):
    return db.query(Category).filter(Category.is_active == True).all()


def find_inactive(db: Session):
    return db.query(Category).filter(Category.is_active == False).all()


def save(db: Session, category: Category):
    db.add(category)
    db.flush()

    return category


ALLOWED_SORT_FIELDS = {
    "name",
    "created_at",
    "updated_at",
}


def find_categories(
    db: Session,
    page: int = 1,
    size: int = 20,
    search: str | None = None,
    is_active: bool | None = None,
    sort_by: str | None = None,
    direction: str = "asc",
):
    query = db.query(Category)

    # -------------------------
    # Filtering
    # -------------------------

    query = apply_filter(
        query,
        Category,
        is_active=is_active,
    )

    # -------------------------
    # Search
    # -------------------------

    query = apply_search(
        query,
        [
            Category.name,
        ],
        search,
    )

    # -------------------------
    # Count before pagination
    # -------------------------

    total_items = query.with_entities(func.count(Category.id)).scalar()

    # -------------------------
    # Safe sorting
    # -------------------------

    if not sort_by or sort_by not in ALLOWED_SORT_FIELDS:
        sort_by = "created_at"

    query = apply_sorting(
        query,
        Category,
        sort_by,
        direction,
    )

    # -------------------------
    # Pagination
    # -------------------------

    items = query.offset((page - 1) * size).limit(size).all()

    return items, total_items
