from sqlalchemy.orm import Session

from datetime import datetime, timezone

from .model import Product

from math import ceil

from app.common.mapper import map_list
from app.common.pagination import PaginationMeta
from app.common.responses import PaginatedResponse
from app.common.entity_utils import get_or_raise

from .schema import (
    ProductCreateRequest,
    ProductUpdateRequest,
    ProductSearchRequest,
)

from .mapper import map_product, map_products

from .repository import find_by_id, find_by_sku, save, find_products

from .exceptions import (
    ProductNotFoundException,
    ProductAlreadyExistsException,
    ProductInactiveException,
)

from .validators import validate_product_hierarchy

from app.logging.logger import logger


def search_products(
    db: Session,
    request: ProductSearchRequest,
):
    products, total_items = find_products(
        db=db,
        page=request.page,
        size=request.size,
        search=request.search,
        supplier_id=request.supplier_id,
        category_id=request.category_id,
        subcategory_id=request.subcategory_id,
        product_type_id=request.product_type_id,
        brand_id=request.brand_id,
        uom_id=request.uom_id,
        is_active=request.is_active,
        sort_by=request.sort_by,
        direction=request.direction,
    )

    total_pages = ceil(total_items / request.size) if total_items > 0 else 0

    pagination = PaginationMeta(
        page=request.page,
        size=request.size,
        total_items=total_items,
        total_pages=total_pages,
        has_next=request.page < total_pages,
        has_previous=request.page > 1,
    )

    return PaginatedResponse(
        items=map_products(products),
        pagination=pagination,
    )


def get_product_by_id(db: Session, product_id: int):
    product = get_or_raise(
        find_by_id(db, product_id),
        ProductNotFoundException("Product not found"),
    )

    return map_product(product)


def create_product(db: Session, request: ProductCreateRequest, current_user_id: int):
    exists = find_by_sku(db, request.sku)

    if exists:
        raise ProductAlreadyExistsException("Product already exists")

    validate_product_hierarchy(
        db,
        request.supplier_id,
        request.category_id,
        request.subcategory_id,
        request.product_type_id,
        request.brand_id,
        request.uom_id,
    )

    product = Product(
        name=request.name,
        description=request.description,
        sku=request.sku,
        barcode=request.barcode,
        supplier_id=request.supplier_id,
        category_id=request.category_id,
        subcategory_id=request.subcategory_id,
        product_type_id=request.product_type_id,
        brand_id=request.brand_id,
        uom_id=request.uom_id,
        purchase_price=request.purchase_price,
        selling_price=request.selling_price,
        created_by=current_user_id,
        is_active=True,
    )

    saved_product = save(db, product)

    db.commit()
    db.refresh(saved_product)

    logger.info(f"Product {saved_product.id} created")

    return map_product(saved_product)


def update_product(
    db: Session, product_id: int, request: ProductUpdateRequest, current_user_id: int
):
    product = get_or_raise(
        find_by_id(db, product_id),
        ProductNotFoundException("Product not found"),
    )

    if not product.is_active:
        raise ProductInactiveException("Product is inactive")

    existing = find_by_sku(db, request.sku)

    if existing and existing.id != product.id:
        raise ProductAlreadyExistsException("SKU already exists")

    validate_product_hierarchy(
        db,
        request.supplier_id,
        request.category_id,
        request.subcategory_id,
        request.product_type_id,
        request.brand_id,
        request.uom_id,
    )

    product.name = request.name
    product.description = request.description
    product.sku = request.sku
    product.barcode = request.barcode

    product.supplier_id = request.supplier_id
    product.category_id = request.category_id
    product.subcategory_id = request.subcategory_id
    product.product_type_id = request.product_type_id

    product.brand_id = request.brand_id
    product.uom_id = request.uom_id

    product.purchase_price = request.purchase_price
    product.selling_price = request.selling_price

    product.updated_by = current_user_id
    product.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(product)

    logger.info(f"Product {product.id} updated")

    return map_product(product)


def deactivate_product(db: Session, product_id: int, current_user_id: int):
    product = get_or_raise(
        find_by_id(db, product_id),
        ProductNotFoundException("Product not found"),
    )

    if not product.is_active:
        return {"message": "Product already inactive"}

    product.is_active = False
    product.deactivated_by = current_user_id
    product.updated_by = current_user_id
    product.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(product)

    logger.info(f"Product {product.id} deactivated")

    return {"message": "Product deactivated successfully"}


def reactivate_product(db: Session, product_id: int, current_user_id: int):
    product = get_or_raise(
        find_by_id(db, product_id),
        ProductNotFoundException("Product not found"),
    )

    if product.is_active:
        return {"message": "Product already active"}

    product.is_active = True
    product.reactivated_by = current_user_id
    product.updated_by = current_user_id
    product.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(product)

    logger.info(f"Product {product.id} reactivated")

    return {"message": "Product reactivated successfully"}
