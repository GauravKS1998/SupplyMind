from sqlalchemy.orm import Session

import math

from datetime import datetime, timezone

from .model import Category

from app.common.pagination import PaginationMeta
from app.common.responses import PaginatedResponse
from app.logging.logger import logger

from app.common.entity_utils import get_or_raise

from .mapper import map_category, map_categories

from .schema import (
    CategoryCreateRequest,
    CategoryUpdateRequest,
    CategoryResponse,
    CategorySearchRequest,
)

from .repository import (
    find_all,
    find_by_id,
    save,
    find_by_name,
    find_active,
    find_inactive,
    find_categories,
)

from .exceptions import (
    CategoryNotFoundException,
    CategoryAlreadyExistsException,
    CategoryInactiveException,
)


def search_categories(
    db: Session, request: CategorySearchRequest
) -> PaginatedResponse[CategoryResponse]:

    categories, total_items = find_categories(
        db=db,
        page=request.page,
        size=request.size,
        search=request.search,
        is_active=request.is_active,
        sort_by=request.sort_by,
        direction=request.direction,
    )

    total_pages = math.ceil(total_items / request.size) if total_items > 0 else 0

    return PaginatedResponse(
        items=map_categories(categories),
        pagination=PaginationMeta(
            page=request.page,
            size=request.size,
            total_items=total_items,
            total_pages=total_pages,
            has_next=request.page < total_pages,
            has_previous=request.page > 1,
        ),
    )


def get_all_categories(db: Session):
    categories = find_all(db)

    return map_categories(categories)


def get_active_categories(db: Session):
    categories = find_active(db)

    return map_categories(categories)


def get_inactive_categories(db: Session):
    categories = find_inactive(db)

    return map_categories(categories)


def create_category(db: Session, request: CategoryCreateRequest, current_user_id: int):

    existing = find_by_name(db, request.name)

    if existing:
        raise CategoryAlreadyExistsException("Category already exists")

    category = Category(name=request.name, created_by=current_user_id)

    saved_category = save(db, category)

    db.commit()
    db.refresh(saved_category)

    logger.info(f"Category {saved_category.id} created")

    return map_category(saved_category)


def update_category(
    db: Session, category_id: int, request: CategoryUpdateRequest, current_user_id: int
):
    category = get_or_raise(
        find_by_id(db, category_id),
        CategoryNotFoundException("Category not found"),
    )

    if not category.is_active:
        raise CategoryInactiveException("Category is inactive")

    category.name = request.name
    category.updated_by = current_user_id
    category.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(category)

    logger.info(f"Category {category.id} updated")

    return map_category(category)


def deactivate_category(db: Session, category_id: int, current_user_id: int):

    category = get_or_raise(
        find_by_id(db, category_id),
        CategoryNotFoundException("Category not found"),
    )

    if not category.is_active:
        return {"message": "Category already inactive"}

    category.is_active = False
    category.updated_by = current_user_id
    category.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(category)

    logger.info(f"Category {category.id} deactivated")

    return {"message": "Category deactivated successfully"}


def reactivate_category(db: Session, category_id: int, current_user_id: int):

    category = get_or_raise(
        find_by_id(db, category_id),
        CategoryNotFoundException("Category not found"),
    )

    if category.is_active:
        return {"message": "Category already active"}

    category.is_active = True
    category.updated_by = current_user_id
    category.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(category)

    logger.info(f"Category {category.id} reactivated")

    return {"message": "Category reactivated successfully"}
