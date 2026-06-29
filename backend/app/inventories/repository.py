from sqlalchemy.orm import Session

from .model import Inventory


def find_all(db: Session):
    return db.query(Inventory).all()


def find_by_id(db: Session, inventory_id=int):
    return db.query(Inventory).filter(Inventory.id == inventory_id).first()


def find_by_product_and_warehouse(db: Session, product_id: int, warehouse_id: int):
    return (
        db.query(Inventory)
        .filter(
            Inventory.product_id == product_id, Inventory.warehouse_id == warehouse_id
        )
        .first()
    )


def save(db: Session, inventory: Inventory):
    db.add(inventory)
    db.commit()
    db.refresh(inventory)

    return inventory


def delete(db: Session, inventory: Inventory):
    db.delete(inventory)
    db.commit()
