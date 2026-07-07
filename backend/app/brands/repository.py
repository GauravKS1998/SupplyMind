from sqlalchemy.orm import Session

from .model import Brand


def find_all(db: Session):
    return db.query(Brand).all()


def find_active(db: Session):
    return db.query(Brand).filter(Brand.is_active == True).all()


def find_inactive(db: Session):
    return db.query(Brand).filter(Brand.is_active == False).all()


def find_by_id(db: Session, brand_id: int):
    return db.query(Brand).filter(Brand.id == brand_id).first()


def find_by_name(db: Session, name: str):
    return db.query(Brand).filter(Brand.name == name).first()


def save(db: Session, brand: Brand):
    db.add(brand)
    db.commit()
    db.refresh(brand)

    return brand
