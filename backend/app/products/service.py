from sqlalchemy.orm import Session

from .schema import (
    ProductResponse, 
    ProductCreateRequest,
    ProductUpdateRequest
)

from .repository import(
    find_all,
    find_by_id,
    save,
    delete
)

def get_all_products(
        db: Session
):
    products = find_all(db)    

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
    product = find_by_id(
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
    product = product(
        name=request.name,
        price=request.price
    )

    saved_product = save(
        db,
        product
    )

    return ProductResponse(
        id = saved_product.id,
        name = saved_product.name,
        price = saved_product.price
    )

def update_product(
        db: Session,
        product_id: int,
        request: ProductUpdateRequest
):
    product = find_by_id(
        db,
        product_id
    )

    if not product:
        return {
            "message": "Product not found"
        }
    
    product.name = request.name
    product.price = request.price

    updated_product = save(
        db,
        product
    )
    
    return ProductResponse(
        id = updated_product.id,
        name = updated_product.name,
        price = updated_product.price
    )

def delete_product(
        db: Session,
        product_id: int
):
    product = find_by_id(
        db,
        product_id
    )

    if not product:
        return {
            "message": "Product not found"
        }
    
    delete(
        db,
        product
    )
    
    return {
        "message": "Product deleted successfully"
    }
