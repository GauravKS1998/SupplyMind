from .model import SubCategory
from .schema import SubCategoryResponse


def map_subcategory(
    subcategory: SubCategory,
) -> SubCategoryResponse:
    return SubCategoryResponse(
        id=subcategory.id,
        name=subcategory.name,
        category_id=subcategory.category_id,
        category_name=subcategory.category.name,
        is_active=subcategory.is_active,
        created_by=subcategory.created_by,
        updated_by=subcategory.updated_by,
        created_at=subcategory.created_at,
        updated_at=subcategory.updated_at,
    )


def map_subcategories(
    subcategories: list[SubCategory],
) -> list[SubCategoryResponse]:
    return [map_subcategory(subcategory) for subcategory in subcategories]
