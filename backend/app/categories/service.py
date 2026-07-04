from sqlalchemy.orm import Session

from .model import Category

from .schema import CategoryCreateRequest, CategoryUpdateRequest, CategoryResponse

from .repository import find_all, find_by_id, save, delete


def get_all_categories(db: Session):
    categories = find_all(db)

    return [
        CategoryResponse(
            id=category.id, name=category.name, created_at=category.created_at
        )
        for category in categories
    ]


def get_category_by_id(db: Session, category_id: int):
    category = find_by_id(db, category_id)

    if not category:
        {"message": "Category not found"}

    return CategoryResponse(
        id=category.id,
        name=category.name,
        created_at=category.created_at,
    )


def create_category(db: Session, request: CategoryCreateRequest):

    category = Category(name=request.name)

    saved_category = save(db, category)

    return CategoryResponse(
        id=saved_category.id,
        name=saved_category.name,
        created_at=saved_category.created_at,
    )


def update_category(db: Session, category_id: int, request: CategoryUpdateRequest):
    category = find_by_id(db, category_id)

    if not category:
        {"message": "Category not found"}

    category.name = request.name

    updated_category = save(db, category)

    return CategoryResponse(
        id=updated_category.id,
        name=updated_category.name,
        created_at=updated_category.created_at,
    )


def delete_category(db: Session, category_id: int):
    category = find_by_id(db, category_id)

    if not category:
        {"message": "Category not found"}

    delete(db, category)

    return {"message": "Category deleted successfully"}
