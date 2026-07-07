from sqlalchemy.orm import Session

from app.suppliers.repository import find_by_id as find_supplier_by_id
from app.categories.repository import find_by_id as find_category_by_id
from app.subcategories.repository import find_by_id as find_subcategory_by_id
from app.product_types.repository import find_by_id as find_product_type_by_id
from app.brands.repository import find_by_id as find_brand_by_id
from app.units_of_measure.repository import (
    find_by_id as find_uom_by_id,
)

from .exceptions import (
    SupplierNotFoundException,
    CategoryNotFoundException,
    SubCategoryNotFoundException,
    ProductTypeNotFoundException,
    BrandNotFoundException,
    UnitOfMeasureNotFoundException,
)


def validate_product_hierarchy(
    db: Session,
    supplier_id: int,
    category_id: int,
    subcategory_id: int,
    product_type_id: int,
    brand_id: int,
    uom_id: int,
):
    supplier = find_supplier_by_id(db, supplier_id)

    if not supplier:
        raise SupplierNotFoundException("Supplier not found")

    if not supplier.is_active:
        raise SupplierNotFoundException("Supplier is inactive")

    category = find_category_by_id(db, category_id)

    if not category:
        raise CategoryNotFoundException("Category not found")

    if not category.is_active:
        raise CategoryNotFoundException("Category is inactive")

    subcategory = find_subcategory_by_id(db, subcategory_id)

    if not subcategory:
        raise SubCategoryNotFoundException("SubCategory not found")

    if not subcategory.is_active:
        raise SubCategoryNotFoundException("SubCategory is inactive")

    if subcategory.category_id != category.id:
        raise SubCategoryNotFoundException("SubCategory does not belong to Category")

    product_type = find_product_type_by_id(db, product_type_id)

    if not product_type:
        raise ProductTypeNotFoundException("Product Type not found")

    if not product_type.is_active:
        raise ProductTypeNotFoundException("Product Type is inactive")

    if product_type.subcategory_id != subcategory.id:
        raise ProductTypeNotFoundException(
            "Product Type does not belong to SubCategory"
        )

    brand = find_brand_by_id(db, brand_id)

    if not brand:
        raise BrandNotFoundException("Brand not found")

    if not brand.is_active:
        raise BrandNotFoundException("Brand is inactive")

    uom = find_uom_by_id(db, uom_id)

    if not uom:
        raise UnitOfMeasureNotFoundException("Unit of Measure not found")

    if not uom.is_active:
        raise UnitOfMeasureNotFoundException("Unit of Measure is inactive")

    return (
        supplier,
        category,
        subcategory,
        product_type,
        brand,
        uom,
    )
