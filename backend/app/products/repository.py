from sqlalchemy.orm import Session
from .model import Product


def find_all(db: Session):
    return db.query(Product).all()


def find_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def find_by_sku(db: Session, sku: str):
    return db.query(Product).filter(Product.sku == sku).first()


def find_by_supplier_id(db: Session, supplier_id: int):
    return (
        db.query(Product)
        .filter(Product.supplier_id == supplier_id, Product.is_active == True)
        .all()
    )


def find_by_category_id(db: Session, category_id: int):
    return (
        db.query(Product)
        .filter(Product.category_id == category_id, Product.is_active == True)
        .all()
    )


def find_by_subcategory_id(db: Session, subcategory_id: int):
    return (
        db.query(Product)
        .filter(Product.subcategory_id == subcategory_id, Product.is_active == True)
        .all()
    )


def find_by_product_type_id(db: Session, product_type_id: int):
    return (
        db.query(Product)
        .filter(Product.product_type_id == product_type_id, Product.is_active == True)
        .all()
    )


def find_active(db: Session):
    return db.query(Product).filter(Product.is_active == True).all()


def find_inactive(db: Session):
    return db.query(Product).filter(Product.is_active == False).all()


def save(db: Session, product: Product):
    db.add(product)
    db.flush()

    return product
