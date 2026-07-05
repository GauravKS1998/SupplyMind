from sqlalchemy.orm import Session

from .model import Warehouse


def save(db: Session, warehouse: Warehouse):
    db.add(warehouse)
    db.commit()
    db.refresh(warehouse)

    return warehouse


def find_by_id(db: Session, warehouse_id: int):
    return db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()


def find_by_code(db: Session, warehouse_code: str):
    return (
        db.query(Warehouse).filter(Warehouse.warehouse_code == warehouse_code).first()
    )


def find_all(db: Session):
    return db.query(Warehouse).all()


def find_all_active(db: Session):
    return db.query(Warehouse).filter(Warehouse.is_active == True).all()


def find_all_inactive(db: Session):
    return db.query(Warehouse).filter(Warehouse.is_active == False).all()
