from sqlalchemy.orm import Session

from datetime import datetime, timezone

from .model import Product

from .schema import ProductResponse, ProductCreateRequest, ProductUpdateRequest

from .repository import (
    find_all,
    find_by_id,
    find_by_sku,
    find_by_barcode,
    save,
    find_by_supplier_id,
    find_by_category_id,
    find_by_subcategory_id,
    find_by_product_type_id,
    find_by_brand_id,
    find_by_uom_id,
    find_active,
    find_inactive,
)

from app.suppliers.repository import find_by_id as find_supplier_by_id
from app.categories.repository import find_by_id as find_category_by_id
from app.subcategories.repository import find_by_id as find_subcategory_by_id
from app.product_types.repository import find_by_id as find_product_type_by_id
from app.brands.repository import find_by_id as find_brand_by_id
from app.units_of_measure.repository import (
    find_by_id as find_uom_by_id,
)

from .exceptions import (
    ProductNotFoundException,
    ProductAlreadyExistsException,
)

from app.categories.exceptions import CategoryNotFoundException
from app.subcategories.exceptions import SubCategoryNotFoundException
from app.product_types.exceptions import ProductTypeNotFoundException
from app.suppliers.exceptions import SupplierNotFoundException
from app.brands.exceptions import BrandNotFoundException
from app.units_of_measure.exceptions import UnitOfMeasureNotFoundException

from .validators import validate_product_hierarchy

from app.logging.logger import logger


def map_product(product: Product):
    return ProductResponse(
        id=product.id,
        name=product.name,
        sku=product.sku,
        description=product.description,
        barcode=product.barcode,
        supplier_id=product.supplier_id,
        supplier_name=product.supplier.name,
        category_id=product.category_id,
        category_name=product.category.name,
        subcategory_id=product.subcategory_id,
        subcategory_name=product.subcategory.name,
        product_type_id=product.product_type_id,
        product_type_name=product.product_type.name,
        brand_id=product.brand_id,
        brand_name=product.brand.name,
        uom_id=product.uom_id,
        uom_code=product.uom.code,
        uom_name=product.uom.name,
        purchase_price=product.purchase_price,
        selling_price=product.selling_price,
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


def get_products_by_brand_id(db: Session, brand_id: int):
    brand = find_brand_by_id(db, brand_id)

    if not brand:
        raise BrandNotFoundException("Brand not found")

    if not brand.is_active:
        raise BrandNotFoundException("Brand is inactive")

    products = find_by_brand_id(db, brand_id)

    return [map_product(product) for product in products]


def get_products_by_uom_id(db: Session, uom_id: int):
    uom = find_uom_by_id(db, uom_id)

    if not uom:
        raise UnitOfMeasureNotFoundException("Unit of Measure not found")

    if not uom.is_active:
        raise UnitOfMeasureNotFoundException("Unit of Measure is inactive")

    products = find_by_uom_id(db, uom_id)

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
        request.brand_id,
        request.uom_id,
    )

    product = Product(
        name=request.name,
        description=request.description,
        sku=request.sku,
        barcode=request.barcode,
        supplier_id=request.supplier_id,
        category_id=request.category_id,
        subcategory_id=request.subcategory_id,
        product_type_id=request.product_type_id,
        brand_id=request.brand_id,
        uom_id=request.uom_id,
        purchase_price=request.purchase_price,
        selling_price=request.selling_price,
        created_by=current_user_id,
        is_active=True,
    )

    saved_product = save(db, product)

    db.commit()
    db.refresh(saved_product)

    logger.info(f"Product {saved_product.id} created")

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
        request.brand_id,
        request.uom_id,
    )

    product.name = request.name
    product.description = request.description
    product.sku = request.sku
    product.barcode = request.barcode

    product.supplier_id = request.supplier_id
    product.category_id = request.category_id
    product.subcategory_id = request.subcategory_id
    product.product_type_id = request.product_type_id

    product.brand_id = request.brand_id
    product.uom_id = request.uom_id

    product.purchase_price = request.purchase_price
    product.selling_price = request.selling_price

    product.updated_by = current_user_id
    product.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(product)

    logger.info(f"Product {product.id} updated")

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

    logger.info(f"Product {product.id} deactivated")

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

    logger.info(f"Product {product.id} reactivated")

    return {"message": "Product reactivated successfully"}
