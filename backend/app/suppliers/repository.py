from sqlalchemy.orm import Session

from .model import Supplier


def save(db: Session, supplier: Supplier):
    db.add(supplier)
    db.commit()
    db.refresh(supplier)

    return supplier


def find_by_id(db: Session, supplier_id: int):
    return db.query(Supplier).filter(Supplier.id == supplier_id).first()


def find_by_user_id(db: Session, user_id: int):
    return db.query(Supplier).filter(Supplier.user_id == user_id).first()


def find_all_pending_verification(db: Session):
    return db.query(Supplier).filter(Supplier.is_verified == False).all()


def find_all(db: Session):
    return db.query(Supplier).all()


def find_all_active(db: Session):
    return db.query(Supplier).filter(Supplier.is_active == True).all()


def find_all_inactive(db: Session):
    return db.query(Supplier).filter(Supplier.is_active == False).all()
