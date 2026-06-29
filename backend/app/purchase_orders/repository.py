from sqlalchemy.orm import Session

from .model import PurchaseOrder


def find_all(db: Session):
    return db.query(PurchaseOrder).all()


def find_by_id(db: Session, purchase_order_id: int):
    return db.query(PurchaseOrder).filter(PurchaseOrder.id == purchase_order_id).first()


def save(db: Session, purchase_order: PurchaseOrder):
    db.add(purchase_order)
    db.commit()
    db.refresh(purchase_order)

    return purchase_order
