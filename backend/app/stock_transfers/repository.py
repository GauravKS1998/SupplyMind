from sqlalchemy.orm import Session

from .model import StockTransfer


def save_transfer(db: Session, transfer: StockTransfer):
    db.add(transfer)
    db.flush()  # temporary save
    """
        unlike
        db.commit() => permanent save
    """

    return transfer
