from datetime import datetime, timezone
from math import ceil

from sqlalchemy.orm import Session

from app.common.pagination import PaginationMeta
from app.common.responses import PaginatedResponse
from app.logging.logger import logger

from .model import Customer

from .schema import (
    CustomerCreateRequest,
    CustomerUpdateRequest,
    CustomerSearchRequest,
)

from .repository import (
    save,
    find_by_id,
    find_by_user_id,
    find_all,
    find_all_active,
    find_all_inactive,
    find_all_pending_verification,
    find_customers,
)

from .mapper import (
    map_customer,
    map_customers,
)

from .validators import (
    validate_customer_exists,
    validate_customer_not_exists_for_user,
    validate_gst_available,
    validate_customer_ownership,
    validate_customer_not_verified,
    validate_customer_not_active,
    validate_customer_not_inactive,
)

from .exceptions import CustomerNotFoundException

# =========================================================
# Get
# =========================================================


def get_customer_by_id(
    db: Session,
    customer_id: int,
):
    customer = validate_customer_exists(
        db,
        customer_id,
    )

    return map_customer(customer)


def get_customer_by_user_id(
    db: Session,
    user_id: int,
):
    customer = find_by_user_id(
        db,
        user_id,
    )

    if not customer:
        raise CustomerNotFoundException("Customer profile not found.")

    return map_customer(customer)


# =========================================================
# Lists
# =========================================================


def get_all_customers(
    db: Session,
):
    customers = find_all(db)

    return map_customers(customers)


def get_active_customers(
    db: Session,
):
    customers = find_all_active(db)

    return map_customers(customers)


def get_inactive_customers(
    db: Session,
):
    customers = find_all_inactive(db)

    return map_customers(customers)


def get_pending_customers(
    db: Session,
):
    customers = find_all_pending_verification(db)

    return map_customers(customers)


# =========================================================
# Search
# =========================================================


def search_customers(
    db: Session,
    request: CustomerSearchRequest,
):
    customers, total_items = find_customers(
        db=db,
        page=request.page,
        size=request.size,
        search=request.search,
        city=request.city,
        state=request.state,
        country=request.country,
        is_verified=request.is_verified,
        is_active=request.is_active,
        sort_by=request.sort_by,
        direction=request.direction,
    )

    total_pages = ceil(total_items / request.size) if total_items > 0 else 0

    return PaginatedResponse(
        items=map_customers(customers),
        pagination=PaginationMeta(
            page=request.page,
            size=request.size,
            total_items=total_items,
            total_pages=total_pages,
            has_next=request.page < total_pages,
            has_previous=request.page > 1,
        ),
    )


# =========================================================
# Create
# =========================================================


def create_customer(
    db: Session,
    request: CustomerCreateRequest,
    current_user_id: int,
):
    validate_customer_not_exists_for_user(
        db,
        current_user_id,
    )

    validate_gst_available(
        db,
        request.gst_number,
    )

    customer = Customer(
        user_id=current_user_id,
        **request.model_dump(),
    )

    saved_customer = save(
        db,
        customer,
    )

    db.commit()
    db.refresh(saved_customer)

    logger.info(
        f"Customer {saved_customer.id} " f"created by user id={current_user_id}."
    )

    return map_customer(saved_customer)


# =========================================================
# Update
# =========================================================


def update_customer(
    db: Session,
    customer_id: int,
    request: CustomerUpdateRequest,
    current_user_id: int,
):
    customer = validate_customer_exists(
        db,
        customer_id,
    )

    validate_customer_ownership(
        customer,
        current_user_id,
    )

    validate_gst_available(
        db,
        request.gst_number,
        customer.id,
    )

    for key, value in request.model_dump().items():
        setattr(
            customer,
            key,
            value,
        )

    customer.updated_by = current_user_id
    customer.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(customer)

    logger.info(f"Customer {customer.id} " f"updated by user id={current_user_id}.")

    return map_customer(customer)


# =========================================================
# Verification
# =========================================================


def verify_customer(
    db: Session,
    customer_id: int,
    current_user_id: int,
):
    customer = validate_customer_exists(
        db,
        customer_id,
    )

    validate_customer_not_verified(
        customer,
    )

    customer.is_verified = True
    customer.verified_by = current_user_id
    customer.updated_by = current_user_id
    customer.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(customer)

    logger.info(f"Customer {customer.id} " f"verified by user id={current_user_id}.")

    return {"message": "Customer verified successfully."}


# =========================================================
# Deactivate
# =========================================================


def deactivate_customer(
    db: Session,
    customer_id: int,
    current_user_id: int,
):
    customer = validate_customer_exists(
        db,
        customer_id,
    )

    validate_customer_not_inactive(
        customer,
    )

    customer.is_active = False
    customer.deactivated_by = current_user_id
    customer.deactivated_at = datetime.now(timezone.utc)
    customer.updated_by = current_user_id
    customer.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(customer)

    logger.info(f"Customer {customer.id} " f"deactivated by user id={current_user_id}.")

    return {"message": "Customer deactivated successfully."}


# =========================================================
# Reactivate
# =========================================================


def reactivate_customer(
    db: Session,
    customer_id: int,
    current_user_id: int,
):
    customer = validate_customer_exists(
        db,
        customer_id,
    )

    validate_customer_not_active(
        customer,
    )

    customer.is_active = True
    customer.reactivated_by = current_user_id
    customer.reactivated_at = datetime.now(timezone.utc)
    customer.updated_by = current_user_id
    customer.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(customer)

    logger.info(f"Customer {customer.id} " f"reactivated by user id={current_user_id}.")

    return {"message": "Customer reactivated successfully."}
