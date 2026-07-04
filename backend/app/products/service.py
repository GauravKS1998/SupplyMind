from sqlalchemy.orm import Session

from .model import Product

from .schema import ProductResponse, ProductCreateRequest, ProductUpdateRequest

from .repository import find_all, find_by_id, save, delete

from app.suppliers.repository import find_by_id as find_supplier_by_id
from app.categories.repository import find_by_id as find_category_by_id
from app.subcategories.repository import find_by_id as find_subcategory_by_id
from app.product_types.repository import find_by_id as find_product_type_by_id


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
        created_at=product.created_at,
    )


def get_all_products(db: Session):
    products = find_all(db)

    return [
        map_product(product) for product in products
    ]  # Equivelent to products.stream().map(...).toList();


def get_product_by_id(db: Session, product_id: int):
    product = find_by_id(db, product_id)

    if not product:
        return {"message": "Product not found"}

    return map_product(product)


def create_product(db: Session, request: ProductCreateRequest):
    supplier = find_supplier_by_id(db, request.supplier_id)

    if not supplier:
        return {"message": "Supplier not found"}

    category = find_category_by_id(db, request.category_id)

    if not category:
        return {"message": "Category not found"}

    subcategory = find_subcategory_by_id(db, request.subcategory_id)

    if not subcategory:
        return {"message": "SubCategory not found"}

    product_type = find_product_type_by_id(db, request.product_type_id)

    if not product_type:
        return {"message": "ProductType not found"}

    product = Product(
        name=request.name,
        sku=request.sku,
        supplier_id=request.supplier_id,
        category_id=request.category_id,
        subcategory_id=request.subcategory_id,
        product_type_id=request.product_type_id,
        price=request.price,
    )

    saved_product = save(db, product)

    return map_product(saved_product)


def update_product(db: Session, product_id: int, request: ProductUpdateRequest):
    product = find_by_id(db, product_id)

    if not product:
        return {"message": "Product not found"}

    product.name = request.name  # Similar to product.setName(...);
    product.sku = request.sku
    product.supplier_id = request.supplier_id
    product.category_id = request.category_id
    product.subcategory_id = request.subcategory_id
    product.product_type_id = request.product_type_id
    product.price = request.price

    updated_product = save(db, product)

    return map_product(updated_product)


def delete_product(db: Session, product_id: int):
    product = find_by_id(db, product_id)

    if not product:
        return {"message": "Product not found"}

    delete(db, product)

    return {"message": "Product deleted successfully"}
