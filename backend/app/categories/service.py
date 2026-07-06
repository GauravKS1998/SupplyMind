from sqlalchemy.orm import Session

from datetime import datetime, timezone

from .model import Category

from .schema import CategoryCreateRequest, CategoryUpdateRequest, CategoryResponse

from .repository import (
    find_all,
    find_by_id,
    save,
    find_by_name,
    find_active,
    find_inactive,
)

from .exceptions import CategoryNotFoundException, CategoryAlreadyExistsException


def get_all_categories(db: Session):
    categories = find_all(db)

    return [
        CategoryResponse.model_validate(category, from_attributes=True)
        for category in categories
    ]


def get_active_categories(db: Session):
    categories = find_active(db)

    return [
        CategoryResponse.model_validate(category, from_attributes=True)
        for category in categories
    ]


def get_inactive_categories(db: Session):
    categories = find_inactive(db)

    return [
        CategoryResponse.model_validate(category, from_attributes=True)
        for category in categories
    ]


def create_category(db: Session, request: CategoryCreateRequest, current_user_id: int):

    existing = find_by_name(db, request.name)

    if existing:
        raise CategoryAlreadyExistsException("Category already exists")

    category = Category(name=request.name, created_by=current_user_id)

    saved_category = save(db, category)

    db.commit()
    db.refresh(saved_category)

    return CategoryResponse.model_validate(saved_category, from_attributes=True)


def update_category(
    db: Session, category_id: int, request: CategoryUpdateRequest, current_user_id: int
):
    category = find_by_id(db, category_id)

    if not category:
        raise CategoryNotFoundException("Category not found")

    category.name = request.name
    category.updated_by = current_user_id
    category.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(category)

    return CategoryResponse.model_validate(category, from_attributes=True)


def deactivate_category(db: Session, category_id: int, current_user_id: int):
    category = find_by_id(db, category_id)

    if not category:
        raise CategoryNotFoundException("Category not found")

    category.is_active = False
    category.updated_by = current_user_id
    category.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(category)

    return {"message": "Category deactivated successfully"}


def reactivate_category(db: Session, category_id: int, current_user_id: int):
    category = find_by_id(db, category_id)

    if not category:
        raise CategoryNotFoundException("Category not found")

    category.is_active = True
    category.updated_by = current_user_id
    category.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(category)

    return {"message": "Category reactivated successfully"}
