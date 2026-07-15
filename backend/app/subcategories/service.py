from sqlalchemy.orm import Session

import math

from datetime import datetime, timezone

from app.common.pagination import PaginationMeta
from app.common.responses import PaginatedResponse
from app.logging.logger import logger

from app.common.entity_utils import get_or_raise

from .model import SubCategory

from .mapper import map_subcategory, map_subcategories

from .schema import (
    SubCategoryCreateRequest,
    SubCategoryUpdateRequest,
    SubCategoryResponse,
    SubCategorySearchRequest,
)

from .repository import (
    find_all,
    find_by_id,
    save,
    find_by_name,
    find_by_category_id,
    find_active,
    find_inactive,
    find_subcategories,
)

from app.categories.repository import find_by_id as find_category_by_id

from .exceptions import (
    SubCategoryNotFoundException,
    SubCategoryAlreadyExistsException,
    SubCategoryInactiveException,
)
from app.categories.exceptions import (
    CategoryNotFoundException,
    CategoryInactiveException,
)


def search_subcategories(
    db: Session,
    request: SubCategorySearchRequest,
) -> PaginatedResponse[SubCategoryResponse]:

    subcategories, total_items = find_subcategories(
        db=db,
        page=request.page,
        size=request.size,
        search=request.search,
        category_id=request.category_id,
        is_active=request.is_active,
        sort_by=request.sort_by,
        direction=request.direction,
    )

    total_pages = math.ceil(total_items / request.size) if total_items > 0 else 0

    return PaginatedResponse(
        items=map_subcategories(subcategories),
        pagination=PaginationMeta(
            page=request.page,
            size=request.size,
            total_items=total_items,
            total_pages=total_pages,
            has_next=request.page < total_pages,
            has_previous=request.page > 1,
        ),
    )


def get_all_subcategories(db: Session):
    subcategories = find_all(db)

    return map_subcategories(subcategories)


def get_active_subcategories(db: Session):
    subcategories = find_active(db)

    return map_subcategories(subcategories)


def get_inactive_subcategories(db: Session):
    subcategories = find_inactive(db)

    return map_subcategories(subcategories)


def get_all_subcategories_by_category(db: Session, category_id: int):

    category = get_or_raise(
        find_by_id(db, category_id),
        CategoryNotFoundException("Category not found"),
    )

    if not category.is_active:
        raise CategoryInactiveException("Category is inactive")

    subcategories = find_by_category_id(db, category_id)

    return map_subcategories(subcategories)


def create_subcategory(
    db: Session, request: SubCategoryCreateRequest, current_user_id: int
):
    category = get_or_raise(
        find_by_id(db, request.category_id),
        CategoryNotFoundException("Category not found"),
    )

    if not category.is_active:
        raise CategoryInactiveException("Category is inactive")

    existing = find_by_name(db, request.name)

    if existing:
        raise SubCategoryAlreadyExistsException("SubCategory already exists")

    subcategory = SubCategory(
        name=request.name, category_id=request.category_id, created_by=current_user_id
    )

    saved_subcategory = save(db, subcategory)

    db.commit()
    db.refresh(saved_subcategory)

    logger.info(f"SubCategory {saved_subcategory.id} created")

    return map_subcategory(saved_subcategory)


def update_subcategory(
    db: Session,
    subcategory_id: int,
    request: SubCategoryUpdateRequest,
    current_user_id: int,
):

    subcategory = get_or_raise(
        find_by_id(db, subcategory_id),
        SubCategoryNotFoundException("SubCategory not found"),
    )

    get_or_raise(
        find_category_by_id(db, request.category_id),
        CategoryNotFoundException("Category not found"),
    )

    if not subcategory.is_active:
        raise SubCategoryInactiveException("SubCategory is inactive")

    subcategory.name = request.name
    subcategory.category_id = request.category_id

    subcategory.updated_by = current_user_id
    subcategory.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(subcategory)

    logger.info(f"SubCategory {subcategory.id} updated")

    return map_subcategory(subcategory)


def deactivate_subcategory(db: Session, subcategory_id: int, current_user_id: int):

    subcategory = get_or_raise(
        find_by_id(db, subcategory_id),
        SubCategoryNotFoundException("SubCategory not found"),
    )

    if not subcategory.is_active:
        return {"message": "SubCategory already inactive"}

    subcategory.is_active = False
    subcategory.updated_by = current_user_id
    subcategory.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(subcategory)

    logger.info(f"SubCategory {subcategory.id} deactivated")

    return {"message": "Subcategory deactivated successfully"}


def reactivate_subcategory(db: Session, subcategory_id: int, current_user_id: int):

    subcategory = get_or_raise(
        find_by_id(db, subcategory_id),
        SubCategoryNotFoundException("SubCategory not found"),
    )

    if subcategory.is_active:
        return {"message": "SubCategory already active"}

    subcategory.is_active = True
    subcategory.updated_by = current_user_id
    subcategory.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(subcategory)

    logger.info(f"SubCategory {subcategory.id} reactivated")

    return {"message": "Subcategory reactivated successfully"}
