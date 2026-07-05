from sqlalchemy.orm import Session

from .model import Customer


def save(db: Session, customer: Customer):
    db.add(customer)
    db.flush()

    return customer


def find_all(db: Session):
    return db.query(Customer).all()


def find_by_id(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()


def find_by_user_id(db: Session, user_id: int):
    return db.query(Customer).filter(Customer.user_id == user_id).first()


def find_active(db: Session):
    return db.query(Customer).filter(Customer.is_active == True).all()


def find_inactive(db: Session):
    return db.query(Customer).filter(Customer.is_active == False).all()


def find_pending(db: Session):
    return db.query(Customer).filter(Customer.is_verified == False).all()
