from sqlalchemy.orm import Session

from .model import ProductType

from .schema import ProductTypeCreateRequest, ProductTypeResponse

from .repository import find_all, find_by_subcategory_id, save

from app.subcategories.repository import find_by_id as find_subcategory_by_id


def map_product_type(product_type: ProductType):
    return ProductTypeResponse(
        id=product_type.id,
        name=product_type.name,
        subcategory_id=product_type.subcategory_id,
        subcategory_name=product_type.subcategory.name,
        created_at=product_type.created_at,
    )


def get_all_product_types(db: Session):
    product_types = find_all(db)

    return [map_product_type(product_type) for product_type in product_types]


def get_all_product_types_by_subcategory(db: Session, subcategory_id: int):
    subcategory = find_by_subcategory_id(db, subcategory_id)

    if not subcategory:
        return {"message": "SubCategory not found"}

    productTypes = find_by_subcategory_id(db, subcategory_id)

    return [map_product_type(productType) for productType in productTypes]


def create_product_type(db: Session, request: ProductTypeCreateRequest):
    subcategory = find_subcategory_by_id(db, request.subcategory_id)

    if not subcategory:
        return {"message": "SubCategory not found"}

    product_type = ProductType(name=request.name, subcategory_id=request.subcategory_id)

    saved_product_type = save(db, product_type)

    return map_product_type(saved_product_type)
