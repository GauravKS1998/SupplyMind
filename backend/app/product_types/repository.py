from sqlalchemy import func
from sqlalchemy.orm import Session

from app.common.filtering import apply_filter
from app.common.search import apply_search
from app.common.sorting import apply_sorting

from .model import ProductType


def find_all(db: Session):
    return db.query(ProductType).all()


def find_by_id(db: Session, product_type_id: int):
    return db.query(ProductType).filter(ProductType.id == product_type_id).first()


def find_by_subcategory_id(
    db: Session,
    subcategory_id: int,
):
    return (
        db.query(ProductType)
        .filter(
            ProductType.subcategory_id == subcategory_id,
        )
        .order_by(ProductType.name.asc())
        .all()
    )


def find_active_by_subcategory_id(
    db: Session,
    subcategory_id: int,
):
    return (
        db.query(ProductType)
        .filter(
            ProductType.subcategory_id == subcategory_id,
            ProductType.is_active.is_(True),
        )
        .order_by(ProductType.name.asc())
        .all()
    )


def find_by_name(db: Session, name: str):
    return db.query(ProductType).filter(ProductType.name == name).first()


def find_active(db: Session):
    return db.query(ProductType).filter(ProductType.is_active == True).all()


def find_inactive(db: Session):
    return db.query(ProductType).filter(ProductType.is_active == False).all()


def save(db: Session, product_type: ProductType):
    db.add(product_type)
    db.flush()

    return product_type


ALLOWED_SORT_FIELDS = {
    "name",
    "created_at",
    "updated_at",
}


def find_product_types(
    db: Session,
    page: int = 1,
    size: int = 20,
    search: str | None = None,
    subcategory_id: int | None = None,
    is_active: bool | None = None,
    sort_by: str | None = None,
    direction: str = "asc",
):
    query = db.query(ProductType)

    # -------------------------
    # Filtering
    # -------------------------

    query = apply_filter(
        query, ProductType, subcategory_id=subcategory_id, is_active=is_active
    )

    # -------------------------
    # Search
    # -------------------------

    query = apply_search(query, [ProductType.name], search)

    # -------------------------
    # Count
    # -------------------------

    total_items = query.with_entities(func.count(ProductType.id)).scalar()

    # -------------------------
    # Safe sorting
    # -------------------------

    if not sort_by or sort_by not in ALLOWED_SORT_FIELDS:
        sort_by = "created_at"

    query = apply_sorting(
        query,
        ProductType,
        sort_by,
        direction,
    )

    # -------------------------
    # Pagination
    # -------------------------

    items = query.offset((page - 1) * size).limit(size).all()

    return items, total_items
