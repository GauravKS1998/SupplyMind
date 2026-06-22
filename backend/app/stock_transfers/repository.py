from sqlalchemy.orm import Session

from .model import StockTransfer

from app.inventories.model import Inventory


def find_inventory(db: Session, product_id: int, warehouse_id: int):
    return (
        db.query(Inventory)
        .filter(
            Inventory.product_id == product_id, Inventory.warehouse_id == warehouse_id
        )
        .first()
    )


def save_transfer(db: Session, transfer: StockTransfer):
    db.add(transfer)
    db.flush()  # temporary save
    """
        unlike
        db.commit() => permanent save
    """

    return transfer
