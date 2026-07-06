from sqlalchemy.orm import Session

from .model import ProductType


def find_all(db: Session):
    return db.query(ProductType).all()


def find_by_id(db: Session, product_type_id: int):
    return db.query(ProductType).filter(ProductType.id == product_type_id).first()


def find_by_subcategory_id(db: Session, subcategory_id: int):
    return (
        db.query(ProductType)
        .filter(
            ProductType.subcategory_id == subcategory_id, ProductType.is_active == True
        )
        .all()
    )


def find_by_name(db: Session, name: str):
    return db.query(ProductType).filter(ProductType.name == name).first()


def find_active(db: Session):
    return db.query(ProductType).filter(ProductType.is_active == True).all()


def find_inactive(db: Session):
    return db.query(ProductType).filter(ProductType.is_active == False).all()


def save(db: Session, product_type: ProductType):
    db.add(product_type)
    db.flush()

    return product_type
