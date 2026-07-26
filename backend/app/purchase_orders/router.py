from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.dependencies import require_roles

from app.purchase_orders.schema import (
    PurchaseOrderCreateRequest,
    PurchaseOrderUpdateRequest,
    PurchaseOrderSearchRequest,
)
from app.purchase_orders.service import (
    create_purchase_order,
    update_purchase_order,
    get_purchase_order,
    search_purchase_orders,
    submit_purchase_order,
    approve_purchase_order,
    reject_purchase_order,
    cancel_purchase_order,
    close_purchase_order,
)

from app.purchase_orders.constants import READ_ROLES, MANAGEMENT_ROLES, APPROVAL_ROLES

router = APIRouter()


@router.post(
    "/search",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def search(
    request: PurchaseOrderSearchRequest,
    db: Session = Depends(get_db),
):
    return search_purchase_orders(
        db,
        request,
    )


@router.get(
    "/{purchase_order_id}",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def get(
    purchase_order_id: int,
    db: Session = Depends(get_db),
):
    return get_purchase_order(
        db,
        purchase_order_id,
    )


@router.post("/")
def create(
    request: PurchaseOrderCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*MANAGEMENT_ROLES)),
):
    return create_purchase_order(
        db,
        request,
        current_user["user_id"],
    )


@router.put("/{purchase_order_id}")
def update(
    purchase_order_id: int,
    request: PurchaseOrderUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*MANAGEMENT_ROLES)),
):
    return update_purchase_order(
        db,
        purchase_order_id,
        request,
        current_user["user_id"],
    )


@router.patch(
    "/{purchase_order_id}/submit",
)
def submit(
    purchase_order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*MANAGEMENT_ROLES)),
):
    return submit_purchase_order(
        db,
        purchase_order_id,
        current_user["user_id"],
    )


@router.patch(
    "/{purchase_order_id}/approve",
)
def approve(
    purchase_order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*APPROVAL_ROLES)),
):
    return approve_purchase_order(
        db,
        purchase_order_id,
        current_user["user_id"],
    )


@router.patch(
    "/{purchase_order_id}/reject",
)
def reject(
    purchase_order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*APPROVAL_ROLES)),
):
    return reject_purchase_order(
        db,
        purchase_order_id,
        current_user["user_id"],
    )


@router.patch(
    "/{purchase_order_id}/cancel",
)
def cancel(
    purchase_order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*MANAGEMENT_ROLES)),
):
    return cancel_purchase_order(
        db,
        purchase_order_id,
        current_user["user_id"],
    )


@router.patch(
    "/{purchase_order_id}/close",
)
def close(
    purchase_order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*MANAGEMENT_ROLES)),
):
    return close_purchase_order(
        db,
        purchase_order_id,
        current_user["user_id"],
    )
