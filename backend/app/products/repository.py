from sqlalchemy import func
from sqlalchemy.orm import Session

from app.common.filtering import apply_filter
from app.common.search import apply_search
from app.common.sorting import apply_sorting

from .model import Product

# -------------------------
# Basic CRUD
# -------------------------


def save(db: Session, product: Product):
    db.add(product)
    db.flush()
    return product


def find_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def find_by_sku(db: Session, sku: str):
    return db.query(Product).filter(Product.sku == sku).first()


# -------------------------
# Product Listing
# -------------------------

ALLOWED_SORT_FIELDS = {
    "name",
    "sku",
    "purchase_price",
    "selling_price",
    "created_at",
    "updated_at",
}


def find_products(
    db: Session,
    page: int = 1,
    size: int = 20,
    search: str | None = None,
    supplier_id: int | None = None,
    category_id: int | None = None,
    subcategory_id: int | None = None,
    product_type_id: int | None = None,
    brand_id: int | None = None,
    uom_id: int | None = None,
    is_active: bool | None = None,
    sort_by: str | None = None,
    direction: str = "asc",
):

    query = db.query(Product)

    # -----------------------
    # Filtering
    # -----------------------

    query = apply_filter(
        query,
        Product,
        supplier_id=supplier_id,
        category_id=category_id,
        subcategory_id=subcategory_id,
        product_type_id=product_type_id,
        brand_id=brand_id,
        uom_id=uom_id,
        is_active=is_active,
    )

    # -----------------------
    # Search
    # -----------------------

    query = apply_search(
        query,
        [
            Product.name,
            Product.sku,
            Product.barcode,
        ],
        search,
    )

    total_items = query.with_entities(func.count(Product.id)).scalar()

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
        Product,
        sort_by,
        direction,
    )

    # -----------------------
    # Pagination
    # -----------------------

    items = query.offset((page - 1) * size).limit(size).all()

    return items, total_items
