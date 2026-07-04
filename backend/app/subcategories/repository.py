from sqlalchemy.orm import Session

from .model import SubCategory


def find_all(db: Session):
    return db.query(SubCategory).all()


def find_by_id(db: Session, subcategory_id: int):
    return db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()


def find_by_category_id(db: Session, category_id: int):
    return db.query(SubCategory).filter(SubCategory.category_id == category_id).all()


def save(db: Session, subcategory: SubCategory):
    db.add(subcategory)
    db.commit()
    db.refresh(subcategory)

    return subcategory
