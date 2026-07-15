from sqlalchemy.orm import Session

import math

from datetime import datetime, timezone

from app.common.pagination import PaginationMeta
from app.common.responses import PaginatedResponse
from app.logging.logger import logger

from app.common.entity_utils import get_or_raise

from .mapper import map_product_type, map_product_types

from .model import ProductType

from .schema import (
    ProductTypeCreateRequest,
    ProductTypeUpdateRequest,
    ProductTypeResponse,
    ProductTypeSearchRequest,
)

from .repository import (
    find_all,
    find_by_id,
    find_by_subcategory_id,
    find_active_by_subcategory_id,
    save,
    find_by_name,
    find_active,
    find_inactive,
    find_product_types,
)

from app.subcategories.repository import find_by_id as find_subcategory_by_id

from .exceptions import (
    ProductTypeNotFoundException,
    ProductTypeAlreadyExistsException,
    ProductTypeInactiveException,
)
from app.subcategories.exceptions import (
    SubCategoryNotFoundException,
    SubCategoryInactiveException,
)


def search_product_types(
    db: Session,
    request: ProductTypeSearchRequest,
) -> PaginatedResponse[ProductTypeResponse]:

    product_types, total_items = find_product_types(
        db=db,
        page=request.page,
        size=request.size,
        search=request.search,
        subcategory_id=request.subcategory_id,
        is_active=request.is_active,
        sort_by=request.sort_by,
        direction=request.direction,
    )

    total_pages = math.ceil(total_items / request.size) if total_items > 0 else 0

    return PaginatedResponse(
        items=map_product_types(product_types),
        pagination=PaginationMeta(
            page=request.page,
            size=request.size,
            total_items=total_items,
            total_pages=total_pages,
            has_next=request.page < total_pages,
            has_previous=request.page > 1,
        ),
    )


def get_all_product_types(db: Session):
    product_types = find_all(db)

    return map_product_types(product_types)


def get_active_product_types(db: Session):
    product_types = find_active(db)

    return map_product_types(product_types)


def get_inactive_product_types(db: Session):
    product_types = find_inactive(db)

    return map_product_types(product_types)


def get_all_product_types_by_subcategory(db: Session, subcategory_id: int):

    subcategory = get_or_raise(
        find_subcategory_by_id(db, subcategory_id),
        SubCategoryNotFoundException("SubCategory not found"),
    )

    product_types = find_by_subcategory_id(db, subcategory.id)

    return map_product_types(product_types)


def get_active_product_types_by_subcategory_id(
    db: Session,
    subcategory_id: int,
):
    subcategory = get_or_raise(
        find_subcategory_by_id(
            db,
            subcategory_id,
        ),
        SubCategoryNotFoundException("SubCategory not found"),
    )

    if not subcategory.is_active:
        raise SubCategoryNotFoundException("SubCategory is inactive")

    product_types = find_active_by_subcategory_id(
        db,
        subcategory.id,
    )

    return map_product_types(product_types)


def create_product_type(
    db: Session, request: ProductTypeCreateRequest, current_user_id: int
):
    subcategory = get_or_raise(
        find_subcategory_by_id(db, request.subcategory_id),
        SubCategoryNotFoundException("SubCategory not found"),
    )

    if not subcategory.is_active:
        raise SubCategoryInactiveException("SubCategory is inactive")

    existing = find_by_name(db, request.name)

    if existing:
        raise ProductTypeAlreadyExistsException("Product-type already exists")

    product_type = ProductType(
        name=request.name,
        subcategory_id=request.subcategory_id,
        created_by=current_user_id,
    )

    saved_product_type = save(db, product_type)

    db.commit()
    db.refresh(saved_product_type)

    logger.info(f"Product-type {saved_product_type.id} created")

    return map_product_type(saved_product_type)


def update_product_type(
    db: Session,
    product_type_id: int,
    request: ProductTypeUpdateRequest,
    current_user_id: int,
):

    product_type = get_or_raise(
        find_by_id(db, product_type_id),
        ProductTypeNotFoundException("Product-type not found"),
    )

    get_or_raise(
        find_subcategory_by_id(db, request.subcategory_id),
        SubCategoryNotFoundException("SubCategory not found"),
    )

    if not product_type.is_active:
        raise ProductTypeInactiveException("Product-type is inactive")

    product_type.name = request.name
    product_type.subcategory_id = request.subcategory_id

    product_type.updated_by = current_user_id
    product_type.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(product_type)

    logger.info(f"Product-type {product_type.id} updated")

    return map_product_type(product_type)


def deactivate_product_type(db: Session, product_type_id: int, current_user_id: int):

    product_type = get_or_raise(
        find_by_id(db, product_type_id),
        ProductTypeNotFoundException("Product-type not found"),
    )

    if not product_type.is_active:
        return {"message": "Product-type already inactive"}

    product_type.is_active = False
    product_type.updated_by = current_user_id
    product_type.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(product_type)

    logger.info(f"Product-type {product_type.id} deactivated")

    return {"message": "Product-type deactivated successfully"}


def reactivate_product_type(db: Session, product_type_id: int, current_user_id: int):

    product_type = get_or_raise(
        find_by_id(db, product_type_id),
        ProductTypeNotFoundException("Product-type not found"),
    )

    if product_type.is_active:
        return {"message": "Product-type already active"}

    product_type.is_active = True
    product_type.updated_by = current_user_id
    product_type.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(product_type)

    logger.info(f"Product-type {product_type.id} reactivated")

    return {"message": "Product-type reactivated successfully"}
