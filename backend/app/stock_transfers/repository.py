from sqlalchemy.orm import Session

from .model import StockTransfer


def save_transfer(db: Session, transfer: StockTransfer):
    db.add(transfer)
    db.flush()  # keep transactional

    return transfer


def find_transfer_by_id(db: Session, transfer_id: int):
    return db.query(StockTransfer).filter(StockTransfer.id == transfer_id).first()
