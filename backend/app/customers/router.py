from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.dependencies import require_roles
from app.auth.enums import UserRole

from .schema import (
    CustomerCreateRequest,
    CustomerUpdateRequest,
)

from .service import (
    create_customer,
    update_customer,
    verify_customer,
    deactivate_customer,
    reactivate_customer,
    get_pending_customers,
    get_active_customers,
    get_inactive_customers,
)

router = APIRouter()


@router.post("/")
def create(
    request: CustomerCreateRequest,
    db: Session = Depends(get_db),
):
    return create_customer(
        db,
        request,
    )


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


@router.put("/{customer_id}/verify")
def verify(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
            UserRole.SALES_MANAGER,
        )
    ),
):
    return verify_customer(
        db,
        customer_id,
        current_user["user_id"],
    )


@router.get(
    "/pending",
    dependencies=[
        Depends(
            require_roles(
                UserRole.ADMIN,
                UserRole.SUPER_ADMIN,
                UserRole.SALES_MANAGER,
            )
        )
    ],
)
def get_pending(
    db: Session = Depends(get_db),
):
    return get_pending_customers(db)


@router.put("/{customer_id}/deactivate")
def deactivate(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
        )
    ),
):
    return deactivate_customer(
        db,
        customer_id,
        current_user["user_id"],
    )


@router.put("/{customer_id}/reactivate")
def reactivate(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
        )
    ),
):
    return reactivate_customer(
        db,
        customer_id,
        current_user["user_id"],
    )


@router.get(
    "/active",
    dependencies=[
        Depends(
            require_roles(
                UserRole.ADMIN,
                UserRole.SUPER_ADMIN,
                UserRole.SALES_MANAGER,
            )
        )
    ],
)
def get_active(
    db: Session = Depends(get_db),
):
    return get_active_customers(db)


@router.get(
    "/inactive",
    dependencies=[
        Depends(
            require_roles(
                UserRole.ADMIN,
                UserRole.SUPER_ADMIN,
                UserRole.SALES_MANAGER,
            )
        )
    ],
)
def get_inactive(
    db: Session = Depends(get_db),
):
    return get_inactive_customers(db)
