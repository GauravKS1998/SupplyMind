from sqlalchemy.orm import Session
from .model import Product


def find_all(db: Session):
    return db.query(Product).all()


def find_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def find_by_sku(db: Session, sku: str):
    return db.query(Product).filter(Product.sku == sku).first()


def find_active(db: Session):
    return db.query(Product).filter(Product.is_active == True).all()


def find_inactive(db: Session):
    return db.query(Product).filter(Product.is_active == False).all()


def save(db: Session, product: Product):
    db.add(product)
    db.flush()

    return product
