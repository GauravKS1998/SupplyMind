from sqlalchemy import and_, func
from sqlalchemy.orm import Session, joinedload

from app.common.filtering import apply_filter
from app.common.search import apply_search
from app.common.sorting import apply_sorting

from app.products.model import Product

from .model import Inventory


def inventory_query(db: Session):
    return db.query(Inventory).options(
        joinedload(Inventory.product).joinedload(Product.supplier),
        joinedload(Inventory.product).joinedload(Product.category),
        joinedload(Inventory.product).joinedload(Product.subcategory),
        joinedload(Inventory.product).joinedload(Product.product_type),
        joinedload(Inventory.warehouse),
    )


def save(db: Session, inventory: Inventory):
    db.add(inventory)
    db.flush()

    return inventory


def find_by_id(db: Session, inventory_id: int):
    return inventory_query(db).filter(Inventory.id == inventory_id).first()


def find_duplicate_inventory(
    db: Session,
    product_id: int,
    warehouse_id: int,
    batch_number: str,
):
    return (
        db.query(Inventory)
        .filter(
            and_(
                Inventory.product_id == product_id,
                Inventory.warehouse_id == warehouse_id,
                Inventory.batch_number == batch_number,
            )
        )
        .first()
    )


def find_all(db: Session):
    return inventory_query(db).order_by(Inventory.created_at.desc()).all()


def find_all_active(db: Session):
    return (
        inventory_query(db)
        .filter(Inventory.is_active.is_(True))
        .order_by(Inventory.created_at.desc())
        .all()
    )


def find_all_inactive(db: Session):
    return (
        inventory_query(db)
        .filter(Inventory.is_active.is_(False))
        .order_by(Inventory.created_at.desc())
        .all()
    )


ALLOWED_SORT_FIELDS = {
    "quantity",
    "available_quantity",
    "reserved_quantity",
    "batch_number",
    "expiry_date",
    "created_at",
    "updated_at",
}


def find_inventories(
    db: Session,
    page: int = 1,
    size: int = 20,
    search: str | None = None,
    warehouse_id: int | None = None,
    product_id: int | None = None,
    batch_number: str | None = None,
    is_active: bool | None = None,
    expiry_before=None,
    expiry_after=None,
    manufacturing_before=None,
    manufacturing_after=None,
    low_stock_only: bool = False,
    sort_by: str | None = None,
    direction: str = "asc",
):
    query = apply_inventory_joins(db.query(Inventory))

    # -------------------------
    # Filtering
    # -------------------------

    query = apply_filter(
        query,
        Inventory,
        warehouse_id=warehouse_id,
        product_id=product_id,
        batch_number=batch_number,
        is_active=is_active,
    )

    if expiry_before:
        query = query.filter(Inventory.expiry_date <= expiry_before)

    if expiry_after:
        query = query.filter(Inventory.expiry_date >= expiry_after)

    if manufacturing_before:
        query = query.filter(Inventory.manufacturing_date <= manufacturing_before)

    if manufacturing_after:
        query = query.filter(Inventory.manufacturing_date >= manufacturing_after)

    if low_stock_only:
        query = query.filter(Inventory.available_quantity <= Inventory.reorder_level)

    # -------------------------
    # Search
    # -------------------------

    query = apply_search(
        query,
        [
            Inventory.batch_number,
            Inventory.storage_location,
        ],
        search,
    )

    # -------------------------
    # Count
    # -------------------------

    total_items = query.with_entities(func.count(Inventory.id)).scalar()

    # -------------------------
    # Sorting
    # -------------------------

    if sort_by not in ALLOWED_SORT_FIELDS:
        sort_by = "created_at"

    query = apply_sorting(
        query,
        Inventory,
        sort_by,
        direction,
    )

    # -------------------------
    # Pagination
    # -------------------------

    items = query.offset((page - 1) * size).limit(size).all()

    return items, total_items
