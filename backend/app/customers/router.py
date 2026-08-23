from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.auth.dependencies import require_roles
from app.database.database import get_db
from app.users.enums import UserRole

from .schema import (
    CustomerCreateRequest,
    CustomerUpdateRequest,
    CustomerSearchRequest,
)

from .constants import (
    READ_ROLES,
    MANAGEMENT_ROLES,
    APPROVAL_ROLES,
)

from .service import (
    create_customer,
    update_customer,
    verify_customer,
    get_customer_by_id,
    get_customer_by_user_id,
    get_all_customers,
    get_pending_customers,
    get_active_customers,
    get_inactive_customers,
    search_customers,
    deactivate_customer,
    reactivate_customer,
)

router = APIRouter()


# =========================================================
# Create
# =========================================================


@router.post("/")
def create(
    request: CustomerCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.CUSTOMER)),
):

    return create_customer(
        db,
        request,
        current_user["user_id"],
    )


# =========================================================
# Search
# =========================================================


@router.post(
    "/search",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def search(
    request: CustomerSearchRequest,
    db: Session = Depends(get_db),
):

    return search_customers(
        db,
        request,
    )


# =========================================================
# All
# =========================================================


@router.get(
    "/",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def get_all(
    db: Session = Depends(get_db),
):

    return get_all_customers(db)


# =========================================================
# Active
# =========================================================


@router.get(
    "/active",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def get_active(
    db: Session = Depends(get_db),
):

    return get_active_customers(db)


# =========================================================
# Inactive
# =========================================================


@router.get(
    "/inactive",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def get_inactive(
    db: Session = Depends(get_db),
):

    return get_inactive_customers(db)


# =========================================================
# Pending Verification
# =========================================================


@router.get(
    "/pending",
    dependencies=[Depends(require_roles(*APPROVAL_ROLES))],
)
def get_pending(
    db: Session = Depends(get_db),
):

    return get_pending_customers(db)


# =========================================================
# Current Customer
# =========================================================


@router.get("/me")
def get_my_customer_profile(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.CUSTOMER)),
):

    return get_customer_by_user_id(
        db,
        current_user["user_id"],
    )


# =========================================================
# Get By ID
# =========================================================


@router.get(
    "/{customer_id}",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def get_by_id(
    customer_id: int,
    db: Session = Depends(get_db),
):

    return get_customer_by_id(
        db,
        customer_id,
    )


# =========================================================
# Update
# =========================================================


@router.put("/{customer_id}")
def update(
    customer_id: int,
    request: CustomerUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.CUSTOMER)),
):

    return update_customer(
        db,
        customer_id,
        request,
        current_user["user_id"],
    )


# =========================================================
# Verify
# =========================================================


@router.put("/{customer_id}/verify")
def verify(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*APPROVAL_ROLES)),
):

    return verify_customer(
        db,
        customer_id,
        current_user["user_id"],
    )


# =========================================================
# Deactivate
# =========================================================


@router.put("/{customer_id}/deactivate")
def deactivate(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*MANAGEMENT_ROLES)),
):

    return deactivate_customer(
        db,
        customer_id,
        current_user["user_id"],
    )


# =========================================================
# Reactivate
# =========================================================


@router.put("/{customer_id}/reactivate")
def reactivate(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*MANAGEMENT_ROLES)),
):

    return reactivate_customer(
        db,
        customer_id,
        current_user["user_id"],
    )
