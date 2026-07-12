from .model import Brand
from .schema import BrandResponse


def map_brand(
    brand: Brand,
) -> BrandResponse:
    return BrandResponse(
        id=brand.id,
        name=brand.name,
        description=brand.description,
        is_active=brand.is_active,
        created_by=brand.created_by,
        updated_by=brand.updated_by,
        deactivated_by=brand.deactivated_by,
        reactivated_by=brand.reactivated_by,
        created_at=brand.created_at,
        updated_at=brand.updated_at,
    )


def map_brands(
    brands: list[Brand],
) -> list[BrandResponse]:
    return [map_brand(brand) for brand in brands]
