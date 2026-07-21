from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.dependencies import require_roles
from app.users.enums import UserRole

from .schema import SalesOrderCreateRequest

from .service import (
    get_all_sales_orders,
    create_draft_sales_order,
    confirm_sales_order,
    reserve_sales_order,
    dispatch_sales_order,
    deliver_sales_order,
    complete_sales_order,
    cancel_sales_order,
    return_sales_order,
)

router = APIRouter()


@router.get("/")
def get_sales_orders(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN,
            UserRole.SALES_MANAGER,
            UserRole.FINANCE_MANAGER,
        )
    ),
):
    return get_all_sales_orders(db)


@router.post("/")
def create(
    request: SalesOrderCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.SUPER_ADMIN,
            UserRole.ADMIN,
            UserRole.SALES_MANAGER,
            UserRole.CUSTOMER,
        )
    ),
):
    return create_draft_sales_order(
        db,
        request,
        current_user["user_id"],
    )


@router.put("/{sales_order_id}/confirm")
def confirm(
    sales_order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.SALES_MANAGER,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
        )
    ),
):
    return confirm_sales_order(
        db,
        sales_order_id,
        current_user["user_id"],
    )


@router.put("/{sales_order_id}/reserve")
def reserve(
    sales_order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.WAREHOUSE_MANAGER,
            UserRole.WAREHOUSE_STAFF,
            UserRole.SUPER_ADMIN,
        )
    ),
):
    return reserve_sales_order(
        db,
        sales_order_id,
        current_user["user_id"],
    )


@router.put("/{sales_order_id}/dispatch")
def dispatch(
    sales_order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.WAREHOUSE_MANAGER,
            UserRole.WAREHOUSE_STAFF,
            UserRole.SUPER_ADMIN,
        )
    ),
):
    return dispatch_sales_order(
        db,
        sales_order_id,
        current_user["user_id"],
    )


@router.put("/{sales_order_id}/deliver")
def deliver(
    sales_order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.SALES_MANAGER,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
        )
    ),
):
    return deliver_sales_order(
        db,
        sales_order_id,
        current_user["user_id"],
    )


@router.put("/{sales_order_id}/complete")
def complete(
    sales_order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.SALES_MANAGER,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
        )
    ),
):
    return complete_sales_order(
        db,
        sales_order_id,
        current_user["user_id"],
    )


@router.put("/{sales_order_id}/cancel")
def cancel(
    sales_order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.CUSTOMER,
            UserRole.SALES_MANAGER,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
        )
    ),
):
    return cancel_sales_order(
        db,
        sales_order_id,
        current_user["user_id"],
    )


@router.put("/{sales_order_id}/return")
def return_order(
    sales_order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.CUSTOMER,
            UserRole.SALES_MANAGER,
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
        )
    ),
):
    return return_sales_order(
        db,
        sales_order_id,
        current_user["user_id"],
    )
