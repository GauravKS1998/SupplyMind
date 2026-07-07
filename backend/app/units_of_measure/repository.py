from sqlalchemy.orm import Session

from .model import UnitOfMeasure


def find_all(db: Session):
    return db.query(UnitOfMeasure).all()


def find_active(db: Session):
    return db.query(UnitOfMeasure).filter(UnitOfMeasure.is_active == True).all()


def find_inactive(db: Session):
    return db.query(UnitOfMeasure).filter(UnitOfMeasure.is_active == False).all()


def find_by_id(db: Session, uom_id: int):
    return db.query(UnitOfMeasure).filter(UnitOfMeasure.id == uom_id).first()


def find_by_name(db: Session, name: str):
    return db.query(UnitOfMeasure).filter(UnitOfMeasure.name == name).first()


def save(db: Session, uom: UnitOfMeasure):
    db.add(uom)
    db.commit()
    db.refresh(uom)

    return uom
