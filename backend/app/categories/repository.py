from sqlalchemy.orm import Session
from .model import Category


def find_all(db: Session):
    return db.query(Category).all()


def find_by_id(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()


def find_by_name(db: Session, name: str):
    return db.query(Category).filter(Category.name == name).first()


def find_active(db: Session):
    return db.query(Category).filter(Category.is_active == True).all()


def find_inactive(db: Session):
    return db.query(Category).filter(Category.is_active == False).all()


def save(db: Session, category: Category):
    db.add(category)
    db.flush()

    return category
