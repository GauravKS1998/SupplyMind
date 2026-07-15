from .model import ProductType
from .schema import ProductTypeResponse


def map_product_type(
    product_type: ProductType,
) -> ProductTypeResponse:
    return ProductTypeResponse(
        id=product_type.id,
        name=product_type.name,
        subcategory_id=product_type.subcategory_id,
        subcategory_name=product_type.subcategory.name,
        is_active=product_type.is_active,
        created_by=product_type.created_by,
        updated_by=product_type.updated_by,
        created_at=product_type.created_at,
        updated_at=product_type.updated_at,
    )


def map_product_types(
    product_types: list[ProductType],
) -> list[ProductTypeResponse]:
    return [map_product_type(product_type) for product_type in product_types]
