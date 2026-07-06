from sqlalchemy.orm import Session

from datetime import datetime, timezone

from .model import SubCategory

from .schema import (
    SubCategoryCreateRequest,
    SubCategoryUpdateRequest,
    SubCategoryResponse,
)

from .repository import (
    find_all,
    find_by_id,
    save,
    find_by_name,
    find_by_category_id,
    find_active,
    find_inactive,
)

from app.categories.repository import find_by_id as find_category_by_id

from .exceptions import (
    SubCategoryNotFoundException,
    SubCategoryAlreadyExistsException,
    CategoryNotFoundException,
)


def map_subcategory(subcategory):
    return SubCategoryResponse(
        id=subcategory.id,
        name=subcategory.name,
        category_id=subcategory.category_id,
        category_name=subcategory.category.name,
        is_active=subcategory.is_active,
        created_at=subcategory.created_at,
        updated_at=subcategory.updated_at,
    )


def get_all_subcategories(db: Session):
    subcategories = find_all(db)

    return [map_subcategory(subcategory) for subcategory in subcategories]


def get_active_subcategories(db: Session):
    subcategories = find_active(db)

    return [map_subcategory(subcategory) for subcategory in subcategories]


def get_inactive_subcategories(db: Session):
    subcategories = find_inactive(db)

    return [map_subcategory(subcategory) for subcategory in subcategories]


def get_all_subcategories_by_category(db: Session, category_id: int):
    category = find_category_by_id(db, category_id)

    if not category:
        raise CategoryNotFoundException("Category not found")

    subcategories = find_by_category_id(db, category_id)

    return [map_subcategory(subcategory) for subcategory in subcategories]


def create_subcategory(
    db: Session, request: SubCategoryCreateRequest, current_user_id: int
):
    category = find_category_by_id(db, request.category_id)

    if not category:
        raise CategoryNotFoundException("Category not found")

    existing = find_by_name(db, request.name)

    if existing:
        raise SubCategoryAlreadyExistsException("SubCategory already exists")

    subcategory = SubCategory(
        name=request.name, category_id=request.category_id, created_by=current_user_id
    )

    saved_subcategory = save(db, subcategory)

    db.commit()
    db.refresh(saved_subcategory)

    return map_subcategory(saved_subcategory)


def update_subcategory(
    db: Session,
    subcategory_id: int,
    request: SubCategoryUpdateRequest,
    current_user_id: int,
):
    subcategory = find_by_id(db, subcategory_id)

    if not subcategory:
        raise SubCategoryNotFoundException("SubCategory not found")

    category = find_category_by_id(db, request.category_id)

    if not category:
        raise CategoryNotFoundException("Category not found")

    subcategory.name = request.name
    subcategory.category_id = request.category_id

    subcategory.updated_by = current_user_id
    subcategory.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(subcategory)

    return map_subcategory(subcategory)


def deactivate_subcategory(db: Session, subcategory_id: int, current_user_id: int):
    subcategory = find_by_id(db, subcategory_id)

    if not subcategory:
        raise SubCategoryNotFoundException("SubCategory not found")

    subcategory.is_active = False
    subcategory.updated_by = current_user_id
    subcategory.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(subcategory)

    return {"message": "Subcategory deactivated successfully"}


def reactivate_subcategory(db: Session, subcategory_id: int, current_user_id: int):
    subcategory = find_by_id(db, subcategory_id)

    if not subcategory:
        raise SubCategoryNotFoundException("SubCategory not found")

    subcategory.is_active = True
    subcategory.updated_by = current_user_id
    subcategory.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(subcategory)

    return {"message": "Subcategory reactivated successfully"}
