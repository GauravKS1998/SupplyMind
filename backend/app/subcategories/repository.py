from sqlalchemy.orm import Session

from .model import SubCategory


def find_all(db: Session):
    return db.query(SubCategory).all()


def find_by_id(db: Session, subcategory_id: int):
    return db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()


def find_by_category_id(db: Session, category_id: int):
    return (
        db.query(SubCategory)
        .filter(SubCategory.category_id == category_id, SubCategory.is_active == True)
        .all()
    )


def find_by_name(db: Session, name: str):
    return db.query(SubCategory).filter(SubCategory.name == name).first()


def find_active(db: Session):
    return db.query(SubCategory).filter(SubCategory.is_active == True).all()


def find_inactive(db: Session):
    return db.query(SubCategory).filter(SubCategory.is_active == False).all()


def save(db: Session, subcategory: SubCategory):
    db.add(subcategory)
    db.flush()

    return subcategory
