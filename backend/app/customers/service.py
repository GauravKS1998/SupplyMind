from sqlalchemy.orm import Session
from datetime import datetime, timezone

from .model import Customer
from .schema import (
    CustomerCreateRequest,
    CustomerUpdateRequest,
    CustomerResponse,
)

from .repository import (
    save,
    find_by_id,
    find_by_user_id,
    find_active,
    find_inactive,
    find_pending,
)

from .exceptions import (
    CustomerNotFoundException,
    CustomerAlreadyExistsException,
    CustomerFailException,
)


def map_customer_response(customer: Customer):
    return CustomerResponse(
        id=customer.id,
        user_id=customer.user_id,
        company_name=customer.company_name,
        gst_number=customer.gst_number,
        contact_person=customer.contact_person,
        phone=customer.phone,
        address=customer.address,
        city=customer.city,
        state=customer.state,
        country=customer.country,
        pincode=customer.pincode,
        is_verified=customer.is_verified,
        is_active=customer.is_active,
        created_at=customer.created_at,
    )


def create_customer(
    db: Session,
    request: CustomerCreateRequest,
):
    existing = find_by_user_id(db, request.user_id)

    if existing:
        raise CustomerAlreadyExistsException("Customer profile already exists")

    try:
        customer = Customer(
            user_id=request.user_id,
            company_name=request.company_name,
            gst_number=request.gst_number,
            contact_person=request.contact_person,
            phone=request.phone,
            address=request.address,
            city=request.city,
            state=request.state,
            country=request.country,
            pincode=request.pincode,
        )

        saved_customer = save(db, customer)

        db.commit()
        db.refresh(saved_customer)

        return map_customer_response(saved_customer)

    except Exception:
        db.rollback()
        raise CustomerFailException("Failed to create customer")


def update_customer(
    db: Session,
    customer_id: int,
    request: CustomerUpdateRequest,
    current_user_id: int,
):
    customer = find_by_id(db, customer_id)

    if not customer:
        raise CustomerNotFoundException("Customer not found")

    if customer.user_id != current_user_id:
        raise CustomerFailException("You are not authorized to update this customer")

    try:
        for key, value in request.model_dump().items():
            setattr(customer, key, value)

        customer.updated_by = current_user_id
        customer.updated_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(customer)

        return map_customer_response(customer)

    except Exception:
        db.rollback()
        raise CustomerFailException("Failed to update customer")


def verify_customer(
    db: Session,
    customer_id: int,
    current_user_id: int,
):
    customer = find_by_id(db, customer_id)

    if not customer:
        raise CustomerNotFoundException("Customer not found")

    customer.is_verified = True
    customer.verified_by = current_user_id

    db.commit()
    db.refresh(customer)

    return {"message": "Customer verified"}


def deactivate_customer(
    db: Session,
    customer_id: int,
    current_user_id: int,
):
    customer = find_by_id(db, customer_id)

    if not customer:
        raise CustomerNotFoundException("Customer not found")

    customer.is_active = False
    customer.deactivated_by = current_user_id

    db.commit()
    db.refresh(customer)

    return {"message": "Customer deactivated"}


def reactivate_customer(
    db: Session,
    customer_id: int,
    current_user_id: int,
):
    customer = find_by_id(db, customer_id)

    if not customer:
        raise CustomerNotFoundException("Customer not found")

    customer.is_active = True
    customer.reactivated_by = current_user_id

    db.commit()
    db.refresh(customer)

    return {"message": "Customer reactivated"}


def get_pending_customers(db: Session):
    customers = find_pending(db)

    return [map_customer_response(c) for c in customers]


def get_active_customers(db: Session):
    customers = find_active(db)

    return [map_customer_response(c) for c in customers]


def get_inactive_customers(db: Session):
    customers = find_inactive(db)

    return [map_customer_response(c) for c in customers]
