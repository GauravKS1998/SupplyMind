from sqlalchemy.orm import Session, joinedload

from .model import PurchaseOrder

from app.products.model import Product


def save(db: Session, purchase_order: PurchaseOrder):
    db.add(purchase_order)
    db.flush()

    return purchase_order


def find_by_id(db: Session, po_id: int):
    return (
        db.query(PurchaseOrder)
        .options(
            joinedload(PurchaseOrder.supplier),
            joinedload(PurchaseOrder.product),
            joinedload(PurchaseOrder.warehouse),
        )
        .filter(PurchaseOrder.id == po_id)
        .first()
    )


def find_by_po_number(db: Session, po_number: str):
    return db.query(PurchaseOrder).filter(PurchaseOrder.po_number == po_number).first()


def find_all(db: Session):
    return (
        db.query(PurchaseOrder)
        .options(
            joinedload(PurchaseOrder.supplier),
            joinedload(PurchaseOrder.product),
            joinedload(PurchaseOrder.warehouse),
        )
        .all()
    )
