from sqlalchemy.orm import Session

from .model import Inventory


def find_all(db: Session):
    return db.query(Inventory).all()


def find_by_id(db: Session, inventory_id=int):
    return db.query(Inventory).filter(Inventory.id == inventory_id).first()


def save(db: Session, inventory: Inventory):
    db.add(inventory)
    db.commit()
    db.refresh(inventory)

    return inventory


def delete(db: Session, inventory: Inventory):
    db.delete(inventory)
    db.commit()
