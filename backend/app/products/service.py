from sqlalchemy.orm import Session

from datetime import datetime, timezone

from .model import Product

from .schema import ProductResponse, ProductCreateRequest, ProductUpdateRequest

from .repository import (
    find_all,
    find_by_id,
    find_by_sku,
    save,
    find_by_supplier_id,
    find_by_category_id,
    find_by_subcategory_id,
    find_by_product_type_id,
    find_active,
    find_inactive,
)

from app.suppliers.repository import find_by_id as find_supplier_by_id
from app.categories.repository import find_by_id as find_category_by_id
from app.subcategories.repository import find_by_id as find_subcategory_by_id
from app.product_types.repository import find_by_id as find_product_type_by_id

from .exceptions import (
    CategoryNotFoundException,
    ProductNotFoundException,
    ProductAlreadyExistsException,
    ProductTypeNotFoundException,
    SubCategoryNotFoundException,
    SupplierNotFoundException,
)

from .validators import validate_product_hierarchy


def map_product(product: Product):
    return ProductResponse(
        id=product.id,
        name=product.name,
        sku=product.sku,
        supplier_id=product.supplier_id,
        supplier_name=product.supplier.name,
        category_id=product.category_id,
        category_name=product.category.name,
        subcategory_id=product.subcategory_id,
        subcategory_name=product.subcategory.name,
        product_type_id=product.product_type_id,
        product_type_name=product.product_type.name,
        price=product.price,
        created_by=product.created_by,
        updated_by=product.updated_by,
        deactivated_by=product.deactivated_by,
        reactivated_by=product.reactivated_by,
        created_at=product.created_at,
        updated_at=product.updated_at,
        is_active=product.is_active,
    )


def get_all_products(db: Session):
    products = find_all(db)

    return [
        map_product(product) for product in products
    ]  # Equivelent to products.stream().map(...).toList();


def get_active_products(db: Session):
    products = find_active(db)

    return [map_product(product) for product in products]


def get_inactive_products(db: Session):
    products = find_inactive(db)

    return [map_product(product) for product in products]


def get_product_by_id(db: Session, product_id: int):
    product = find_by_id(db, product_id)

    if not product:
        raise ProductNotFoundException("Product not found")

    return map_product(product)


def get_products_by_supplier_id(db: Session, supplier_id: int):
    supplier = find_supplier_by_id(db, supplier_id)

    if not supplier:
        raise SupplierNotFoundException("Supplier not found")

    products = find_by_supplier_id(db, supplier_id)

    return [map_product(product) for product in products]


def get_products_by_category_id(db: Session, category_id: int):
    category = find_category_by_id(db, category_id)

    if not category:
        raise CategoryNotFoundException("Category not found")

    products = find_by_category_id(db, category_id)

    return [map_product(product) for product in products]


def get_products_by_subcategory_id(db: Session, subcategory_id: int):
    subcategory = find_subcategory_by_id(db, subcategory_id)

    if not subcategory:
        raise SubCategoryNotFoundException("SubCategory not found")

    products = find_by_subcategory_id(db, subcategory_id)

    return [map_product(product) for product in products]


def get_products_by_product_type_id(db: Session, product_type_id: int):
    product_type = find_product_type_by_id(db, product_type_id)

    if not product_type:
        raise ProductTypeNotFoundException("Product type not found")

    products = find_by_product_type_id(db, product_type_id)

    return [map_product(product) for product in products]


def create_product(db: Session, request: ProductCreateRequest, current_user_id: int):
    exists = find_by_sku(db, request.sku)

    if exists:
        raise ProductAlreadyExistsException("Product already exists")

    validate_product_hierarchy(
        db,
        request.supplier_id,
        request.category_id,
        request.subcategory_id,
        request.product_type_id,
    )

    product = Product(
        name=request.name,
        sku=request.sku,
        supplier_id=request.supplier_id,
        category_id=request.category_id,
        subcategory_id=request.subcategory_id,
        product_type_id=request.product_type_id,
        price=request.price,
        is_active=True,
        created_by=current_user_id,
    )

    saved_product = save(db, product)

    db.commit()
    db.refresh(saved_product)

    return map_product(saved_product)


def update_product(
    db: Session, product_id: int, request: ProductUpdateRequest, current_user_id: int
):
    product = find_by_id(db, product_id)

    if not product:
        raise ProductNotFoundException("Product not found")

    if not product.is_active:
        raise ProductNotFoundException("Product is inactive")

    existing = find_by_sku(db, request.sku)

    if existing and existing.id != product.id:
        raise ProductAlreadyExistsException("SKU already exists")

    validate_product_hierarchy(
        db,
        request.supplier_id,
        request.category_id,
        request.subcategory_id,
        request.product_type_id,
    )

    product.name = request.name  # Similar to product.setName(...);
    product.sku = request.sku
    product.supplier_id = request.supplier_id
    product.category_id = request.category_id
    product.subcategory_id = request.subcategory_id
    product.product_type_id = request.product_type_id
    product.price = request.price

    product.updated_by = current_user_id
    product.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(product)

    return map_product(product)


def deactivate_product(db: Session, product_id: int, current_user_id: int):
    product = find_by_id(db, product_id)

    if not product:
        raise ProductNotFoundException("Product not found")

    if not product.is_active:
        return {"message": "Product already inactive"}

    product.is_active = False
    product.deactivated_by = current_user_id
    product.updated_by = current_user_id
    product.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(product)

    return {"message": "Product deactivated successfully"}


def reactivate_product(db: Session, product_id: int, current_user_id: int):
    product = find_by_id(db, product_id)

    if not product:
        raise ProductNotFoundException("Product not found")

    if product.is_active:
        return {"message": "Product already active"}

    product.is_active = True
    product.reactivated_by = current_user_id
    product.updated_by = current_user_id
    product.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(product)

    return {"message": "Product reactivated successfully"}
