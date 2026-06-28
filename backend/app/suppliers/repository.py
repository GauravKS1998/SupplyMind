from sqlalchemy.orm import Session

from .model import Supplier


def find_all(db: Session):
    return db.query(Supplier).all()


def find_by_id(db: Session, supplier_id: int):
    return db.query(Supplier).filter(Supplier.id == supplier_id).first()


def save(db: Session, supplier: Supplier):
    db.add(supplier)
    db.commit()
    db.refresh(supplier)

    return supplier


def delete(db: Session, supplier: Supplier):
    db.delete(supplier)
    db.commit()
