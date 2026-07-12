from .model import Product
from .schema import ProductResponse


def map_product(product: Product) -> ProductResponse:
    return ProductResponse(
        id=product.id,
        name=product.name,
        sku=product.sku,
        barcode=product.barcode,
        description=product.description,
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
        is_active=product.is_active,
        created_by=product.created_by,
        updated_by=product.updated_by,
        deactivated_by=product.deactivated_by,
        reactivated_by=product.reactivated_by,
        created_at=product.created_at,
        updated_at=product.updated_at,
    )


def map_products(products: list[Product]) -> list[ProductResponse]:
    return [map_product(product) for product in products]
