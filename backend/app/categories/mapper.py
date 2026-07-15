from .model import Category
from .schema import CategoryResponse


def map_category(
    category: Category,
) -> CategoryResponse:
    return CategoryResponse(
        id=category.id,
        name=category.name,
        is_active=category.is_active,
        created_by=category.created_by,
        updated_by=category.updated_by,
        created_at=category.created_at,
        updated_at=category.updated_at,
    )


def map_categories(
    categories: list[Category],
) -> list[CategoryResponse]:
    return [map_category(category) for category in categories]
