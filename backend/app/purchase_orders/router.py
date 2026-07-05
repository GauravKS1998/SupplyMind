from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from .schema import PurchaseOrderCreateRequest

from .service import (
    create_draft_po,
    submit_po,
    approve_po,
    reject_po,
    mark_ordered,
    mark_in_transit,
    receive_po,
    close_po,
    cancel_po,
)

from app.auth.dependencies import require_roles
from app.auth.enums import UserRole

router = APIRouter()


@router.post("/")
def create(
    request: PurchaseOrderCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.SUPER_ADMIN, UserRole.PROCUREMENT_MANAGER)
    ),
):
    return create_draft_po(db, request, current_user["user_id"])


@router.put("/{po_id}/submit")
def submit(
    po_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.SUPER_ADMIN, UserRole.PROCUREMENT_MANAGER)
    ),
):
    return submit_po(db, po_id, current_user["user_id"])


@router.put("/{po_id}/approve")
def approve(
    po_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.FINANCE_MANAGER)
    ),
):
    return approve_po(db, po_id, current_user["user_id"])


@router.put("/{po_id}/reject")
def reject(
    po_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.FINANCE_MANAGER)
    ),
):
    return reject_po(db, po_id, current_user["user_id"])


@router.put("/{po_id}/ordered")
def ordered(
    po_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.SUPER_ADMIN, UserRole.PROCUREMENT_MANAGER)
    ),
):
    return mark_ordered(db, po_id, current_user["user_id"])


@router.put("/{po_id}/in-transit")
def in_transit(
    po_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.SUPER_ADMIN, UserRole.SUPPLIER, UserRole.PROCUREMENT_MANAGER
        )
    ),
):
    return mark_in_transit(db, po_id, current_user["user_id"])


@router.put("/{po_id}/receive")
def receive(
    po_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.SUPER_ADMIN, UserRole.WAREHOUSE_STAFF, UserRole.WAREHOUSE_MANAGER
        )
    ),
):
    return receive_po(db, po_id, current_user["user_id"])


@router.put("/{po_id}/close")
def close(
    po_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.PROCUREMENT_MANAGER
        )
    ),
):
    return close_po(db, po_id, current_user["user_id"])


@router.put("/{po_id}/cancel")
def cancel(
    po_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.PROCUREMENT_MANAGER
        )
    ),
):
    return cancel_po(db, po_id, current_user["user_id"])
