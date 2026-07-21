from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.auth.dependencies import require_roles
from app.users.enums import UserRole
from app.database.database import get_db

from .service import (
    initiate_transfer,
    approve_transfer,
    reject_transfer,
    mark_in_transit,
    complete_transfer,
    cancel_transfer,
)

from .schema import StockTransferRequest

router = APIRouter()


@router.post("/")
def initiate(
    request: StockTransferRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.WAREHOUSE_MANAGER, UserRole.WAREHOUSE_STAFF, UserRole.SUPER_ADMIN
        )
    ),
):
    return initiate_transfer(db, request, current_user["user_id"])


@router.put("/{transfer_id}/approve")
def approve(
    transfer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.WAREHOUSE_MANAGER, UserRole.ADMIN, UserRole.SUPER_ADMIN)
    ),
):
    return approve_transfer(db, transfer_id, current_user["user_id"])


@router.put("/{transfer_id}/reject")
def reject(
    transfer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.WAREHOUSE_MANAGER, UserRole.ADMIN, UserRole.SUPER_ADMIN)
    ),
):
    return reject_transfer(db, transfer_id, current_user["user_id"])


@router.put("/{transfer_id}/in-transit")
def move_to_transit(
    transfer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.WAREHOUSE_MANAGER, UserRole.WAREHOUSE_STAFF, UserRole.SUPER_ADMIN
        )
    ),
):
    return mark_in_transit(db, transfer_id, current_user["user_id"])


@router.put("/{transfer_id}/complete")
def complete(
    transfer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.WAREHOUSE_MANAGER, UserRole.WAREHOUSE_STAFF, UserRole.SUPER_ADMIN
        )
    ),
):
    return complete_transfer(db, transfer_id, current_user["user_id"])


@router.put("/{transfer_id}/cancel")
def cancel(
    transfer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.WAREHOUSE_MANAGER, UserRole.ADMIN, UserRole.SUPER_ADMIN)
    ),
):
    return cancel_transfer(db, transfer_id, current_user["user_id"])
