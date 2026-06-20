from sqlalchemy.orm import Session

from .schema import (
    ProductResponse, 
    ProductCreateRequest,
    ProductUpdateRequest
)

from .repository import(
    get_all_products as repo_get_all_products,
    create_product as repo_create_product,
    get_product_by_id as repo_get_product_by_id,
    update_product as repo_update_product,
    delete_product as repo_delete_product
)

def get_all_products(
        db: Session
):
    products = repo_get_all_products(db)    

    return [
        ProductResponse(
            id = product.id,
            name = product.name,
            price = product.price
        )
        for product in products
    ] # Equivelent to products.stream().map(...).toList();

def get_product_by_id(
        db: Session,
        product_id: int
):
    product = repo_get_product_by_id(
        db,
        product_id
    )

    if not product:
        return {
            "message": "Product not found"
        }
    
    return ProductResponse(
        id = product.id,
        name = product.name,
        price = product.price
    )

def create_product(
        db: Session,
        request: ProductCreateRequest
):
    product = repo_create_product(
        db,
        request.name,
        request.price
    )

    return ProductResponse(
        id = product.id,
        name = product.name,
        price = product.price
    )

def update_product(
        db: Session,
        product_id: int,
        request: ProductUpdateRequest
):
    product = repo_update_product(
        db,
        product_id,
        request.name,
        request.price
    )

    if not product:
        return {
            "message": "Product not found"
        }
    
    return ProductResponse(
        id = product.id,
        name = product.name,
        price = product.price
    )

def delete_product(
        db: Session,
        product_id: int
):
    product = repo_delete_product(
        db,
        product_id
    )

    if not product:
        return {
            "message": "Product not found"
        }
    
    return {
        "message": "Product deleted successfully"
    }
