from sqlalchemy.orm import Session

from app.common.entity_utils import get_or_raise

from .repository import (
    find_by_id,
    find_by_user_id,
    find_by_gst_number,
)

from .model import Customer

from .exceptions import (
    CustomerAlreadyExistsException,
    CustomerNotFoundException,
    CustomerAccessDeniedException,
    InvalidCustomerStateException,
)


def validate_customer_exists(
    db: Session,
    customer_id: int,
):

    customer = get_or_raise(
        find_by_id(
            db,
            customer_id,
        ),
        CustomerNotFoundException(f"Customer '{customer_id}' not found."),
    )

    return customer


def validate_customer_not_exists_for_user(
    db: Session,
    user_id: int,
):

    existing = find_by_user_id(
        db,
        user_id,
    )

    if existing:
        raise CustomerAlreadyExistsException(
            "Customer profile already exists for this user."
        )


def validate_gst_available(
    db: Session,
    gst_number: str | None,
    customer_id: int | None = None,
):

    if not gst_number:
        return

    existing = find_by_gst_number(
        db,
        gst_number,
    )

    if existing and existing.id != customer_id:
        raise CustomerAlreadyExistsException(
            "A customer with this GST number already exists."
        )


def validate_customer_ownership(
    customer: Customer,
    current_user_id: int,
):

    if customer.user_id != current_user_id:
        raise CustomerAccessDeniedException(
            "You are not authorized to modify this customer."
        )


def validate_customer_active(
    customer: Customer,
):

    if not customer.is_active:
        raise InvalidCustomerStateException("Customer account is inactive.")


def validate_customer_not_verified(
    customer: Customer,
):

    if customer.is_verified:
        raise InvalidCustomerStateException("Customer is already verified.")


def validate_customer_not_active(
    customer: Customer,
):

    if customer.is_active:
        raise InvalidCustomerStateException("Customer is already active.")


def validate_customer_not_inactive(
    customer: Customer,
):

    if not customer.is_active:
        raise InvalidCustomerStateException("Customer is already inactive.")
