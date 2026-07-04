from sqlalchemy.orm import Session

from .model import SubCategory

from .schema import SubCategoryCreateRequest, SubCategoryResponse

from .repository import find_all, find_by_category_id, save

from app.categories.repository import find_by_id as find_category_by_id


def map_subcategory(subcategory: SubCategory):
    return SubCategoryResponse(
        id=subcategory.id,
        name=subcategory.name,
        category_id=subcategory.category_id,
        category_name=subcategory.category.name,
        created_at=subcategory.created_at,
    )


def get_all_subcategories(db: Session):
    subcategories = find_all(db)

    return [map_subcategory(subcategory) for subcategory in subcategories]


def get_all_subcategories_by_category(db: Session, category_id: int):
    category = find_category_by_id(db, category_id)

    if not category:
        return {"message": "Category not found"}

    subcategories = find_by_category_id(db, category_id)

    return [map_subcategory(subcategory) for subcategory in subcategories]


def create_subcategory(db: Session, request: SubCategoryCreateRequest):
    category = find_category_by_id(db, request.category_id)

    if not category:
        return {"message": "Category not found"}

    subcategory = SubCategory(name=request.name, category_id=request.category_id)

    saved_subcategory = save(db, subcategory)

    return map_subcategory(saved_subcategory)
