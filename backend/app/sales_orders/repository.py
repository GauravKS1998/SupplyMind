from sqlalchemy.orm import Session

from .model import SalesOrder


def save(db: Session, sales_order: SalesOrder):
    db.add(sales_order)
    db.flush()

    return sales_order


def find_all(db: Session):
    return db.query(SalesOrder).all()
