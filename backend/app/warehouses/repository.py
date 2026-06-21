from sqlalchemy.orm import Session
from .model import Warehouse


def find_all(db: Session):
    return db.query(Warehouse).all()


def find_by_id(db: Session, warehouse_id: int):
    return db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()


def save(db: Session, warehouse: Warehouse):
    db.add(warehouse)
    db.commit()
    db.refresh(warehouse)

    return warehouse


def delete(db: Session, warehouse: Warehouse):
    db.delete(warehouse)
    db.commit()
