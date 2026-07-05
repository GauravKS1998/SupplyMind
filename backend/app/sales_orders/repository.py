from sqlalchemy.orm import Session, joinedload

from .model import SalesOrder


def save(db: Session, sales_order: SalesOrder):
    db.add(sales_order)
    db.flush()

    return sales_order


def find_all(db: Session):
    return (
        db.query(SalesOrder)
        .options(joinedload(SalesOrder.product), joinedload(SalesOrder.warehouse))
        .all()
    )


def find_by_id(db: Session, sales_order_id: int):
    return (
        db.query(SalesOrder)
        .options(joinedload(SalesOrder.product), joinedload(SalesOrder.warehouse))
        .filter(SalesOrder.id == sales_order_id)
        .first()
    )


def find_by_so_number(db: Session, so_number: str):
    return db.query(SalesOrder).filter(SalesOrder.so_number == so_number).first()
