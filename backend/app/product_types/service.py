from sqlalchemy.orm import Session

from datetime import datetime, timezone

from .model import ProductType

from .schema import (
    ProductTypeCreateRequest,
    ProductTypeUpdateRequest,
    ProductTypeResponse,
)

from .repository import (
    find_all,
    find_by_id,
    find_by_subcategory_id,
    save,
    find_by_name,
    find_active,
    find_inactive,
)

from app.subcategories.repository import find_by_id as find_subcategory_by_id

from .exceptions import (
    ProductTypeNotFoundException,
    ProductTypeAlreadyExistsException,
)
from app.subcategories.exceptions import SubCategoryNotFoundException


def map_product_type(product_type):
    return ProductTypeResponse(
        id=product_type.id,
        name=product_type.name,
        subcategory_id=product_type.subcategory_id,
        subcategory_name=product_type.subcategory.name,
        is_active=product_type.is_active,
        created_at=product_type.created_at,
        updated_at=product_type.updated_at,
    )


def get_all_product_types(db: Session):
    product_types = find_all(db)

    return [map_product_type(product_type) for product_type in product_types]


def get_active_product_types(db: Session):
    product_types = find_active(db)

    return [map_product_type(product_type) for product_type in product_types]


def get_inactive_product_types(db: Session):
    product_types = find_inactive(db)

    return [map_product_type(product_type) for product_type in product_types]


def get_all_product_types_by_subcategory(db: Session, subcategory_id: int):
    subcategory = find_subcategory_by_id(db, subcategory_id)

    if not subcategory:
        raise SubCategoryNotFoundException("SubCategory not found")

    productTypes = find_by_subcategory_id(db, subcategory_id)

    return [map_product_type(productType) for productType in productTypes]


def create_product_type(
    db: Session, request: ProductTypeCreateRequest, current_user_id: int
):
    subcategory = find_subcategory_by_id(db, request.subcategory_id)

    if not subcategory:
        raise SubCategoryNotFoundException("SubCategory not found")

    existing = find_by_name(db, request.name)

    if existing:
        raise ProductTypeAlreadyExistsException("Product-type already exists")

    product_type = ProductType(
        name=request.name,
        subcategory_id=request.subcategory_id,
        created_by=current_user_id,
    )

    saved_product_type = save(db, product_type)

    db.commit()
    db.refresh(saved_product_type)

    return map_product_type(saved_product_type)


def update_product_type(
    db: Session,
    product_type_id: int,
    request: ProductTypeUpdateRequest,
    current_user_id: int,
):
    product_type = find_by_id(db, product_type_id)

    if not product_type:
        raise ProductTypeNotFoundException("Product-type not found")

    subcategory = find_subcategory_by_id(db, request.subcategory_id)

    if not subcategory:
        raise SubCategoryNotFoundException("SubCategory not found")

    product_type.name = request.name
    product_type.subcategory_id = request.subcategory_id

    product_type.updated_by = current_user_id
    product_type.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(product_type)

    return map_product_type(product_type)


def deactivate_product_type(db: Session, product_type_id: int, current_user_id: int):
    product_type = find_by_id(db, product_type_id)

    if not product_type:
        raise ProductTypeNotFoundException("Product-type not found")

    product_type.is_active = False
    product_type.updated_by = current_user_id
    product_type.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(product_type)

    return {"message": "Product-type deactivated successfully"}


def reactivate_product_type(db: Session, product_type_id: int, current_user_id: int):
    product_type = find_by_id(db, product_type_id)

    if not product_type:
        raise ProductTypeNotFoundException("Product-type not found")

    product_type.is_active = True
    product_type.updated_by = current_user_id
    product_type.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(product_type)

    return {"message": "Product-type reactivated successfully"}
