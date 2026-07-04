from sqlalchemy.orm import Session

from .model import Category


def find_all(db: Session):
    return db.query(Category).all()


def find_by_id(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()


def save(db: Session, category: Category):
    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def delete(db: Session, category: Category):
    db.delete(category)
    db.commit()
