from datetime import datetime, timezone
from math import ceil

from sqlalchemy.orm import Session

from .model import Brand

from app.common.entity_utils import get_or_raise
from app.common.pagination import PaginationMeta
from app.common.responses import PaginatedResponse
from app.logging.logger import logger

from .schema import BrandCreateRequest, BrandUpdateRequest, BrandSearchRequest

from .repository import (
    find_brands,
    save,
    find_by_id,
    find_by_name,
)

from .exceptions import (
    BrandAlreadyExistsException,
    BrandNotFoundException,
    BrandInactiveException,
)

from .mapper import (
    map_brand,
    map_brands,
)


def search_brands(
    db: Session,
    request: BrandSearchRequest,
):
    brands, total_items = find_brands(
        db=db,
        page=request.page,
        size=request.size,
        search=request.search,
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
        items=map_brands(brands),
        pagination=pagination,
    )


def get_brand_by_id(db: Session, brand_id: int):

    brand = get_or_raise(
        find_by_id(db, brand_id),
        BrandNotFoundException("Brand not found"),
    )

    return map_brand(brand)


def create_brand(
    db: Session,
    request: BrandCreateRequest,
    current_user_id: int,
):

    existing = find_by_name(db, request.name)

    if existing:
        raise BrandAlreadyExistsException("Brand already exists")

    brand = Brand(
        name=request.name,
        description=request.description,
        created_by=current_user_id,
        is_active=True,
    )

    saved_brand = save(db, brand)

    db.commit()
    db.refresh(saved_brand)

    logger.info(f"Brand {saved_brand.id} created")

    return map_brand(saved_brand)


def update_brand(
    db: Session,
    brand_id: int,
    request: BrandUpdateRequest,
    current_user_id: int,
):

    brand = get_or_raise(
        find_by_id(db, brand_id),
        BrandNotFoundException("Brand not found"),
    )

    if not brand.is_active:
        raise BrandInactiveException("Brand is inactive")

    existing = find_by_name(db, request.name)

    if existing and existing.id != brand.id:
        raise BrandAlreadyExistsException("Brand already exists")

    brand.name = request.name.strip()
    brand.description = request.description

    brand.updated_by = current_user_id
    brand.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(brand)

    logger.info(f"Brand {brand.id} updated")

    return map_brand(brand)


def deactivate_brand(
    db: Session,
    brand_id: int,
    current_user_id: int,
):

    brand = get_or_raise(
        find_by_id(db, brand_id),
        BrandNotFoundException("Brand not found"),
    )

    if not brand.is_active:
        return {"message": "Brand already inactive"}

    brand.is_active = False

    brand.deactivated_by = current_user_id
    brand.updated_by = current_user_id
    brand.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(brand)

    logger.info(f"Brand {brand.id} deactivated")

    return {"message": "Brand deactivated successfully"}


def reactivate_brand(
    db: Session,
    brand_id: int,
    current_user_id: int,
):

    brand = get_or_raise(
        find_by_id(db, brand_id),
        BrandNotFoundException("Brand not found"),
    )

    if brand.is_active:
        return {"message": "Brand already active"}

    brand.is_active = True

    brand.reactivated_by = current_user_id
    brand.updated_by = current_user_id
    brand.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(brand)

    logger.info(f"Brand {brand.id} reactivated")

    return {"message": "Brand activated successfully"}
