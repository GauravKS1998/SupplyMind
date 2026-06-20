from sqlalchemy.orm import Session

from .model import Product

def get_all_products(
        db: Session # Similar to EntityManager/JpaRepository
): 
    return db.query(Product).all() # Similar to productRepository.findAll()

def get_product_by_id(
        db: Session,
        product_id: int
):
    return db.query(Product).filter(
        Product.id == product_id
    ).first() # Similar to productRepository.findById(id)

def create_product(
        db: Session, # Similar to EntityManager/JpaRepository
        name: str,
        price: float
):
    product = Product( # Similar to new Product()
        name = name,
        price = price
    )

    db.add(product) # similar to repository.save(product)
    db.commit() # Equivalent to transaction commit
    db.refresh(product) # Equivalent to entityManager.refresh(entity)

    return product

def update_product(
        db: Session,
        product_id: int,
        name: str,
        price: float
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        return None
    
    product.name = name # Similar to product.setName(...);
    product.price = price # Similar to product.setPrice(...);

    db.commit() # Similar to repository.save(product);
    db.refresh(product)

    return product

def delete_product(
        db: Session,
        product_id: int
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        return None
    
    db.delete(product) # Similar to repository.delete(entity);
    db.commit()

    return product