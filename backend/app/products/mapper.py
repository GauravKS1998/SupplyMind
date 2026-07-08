from .model import Product
from .schema import ProductResponse


def map_product(product: Product) -> ProductResponse:
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
        brand_id=product.brand_id,
        brand_name=product.brand.name,
        unit_of_measure_id=product.unit_of_measure_id,
        unit_of_measure_code=product.unit_of_measure.code,
        unit_of_measure_name=product.unit_of_measure.name,
        purchase_price=product.purchase_price,
        selling_price=product.selling_price,
        barcode=product.barcode,
        created_by=product.created_by,
        updated_by=product.updated_by,
        deactivated_by=product.deactivated_by,
        reactivated_by=product.reactivated_by,
        created_at=product.created_at,
        updated_at=product.updated_at,
        is_active=product.is_active,
    )


def map_products(products: list[Product]) -> list[ProductResponse]:
    return [map_product(product) for product in products]
