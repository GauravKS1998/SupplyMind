from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.dependencies import require_roles

from app.stock_transfers.schema import (
    StockTransferCreateRequest,
    StockTransferUpdateRequest,
    StockTransferSearchRequest,
    StockTransferApproveRequest,
    StockTransferRejectRequest,
    StockTransferTransitRequest,
    StockTransferCompleteRequest,
    StockTransferCancelRequest,
)

from app.stock_transfers.service import (
    create_stock_transfer,
    update_stock_transfer,
    get_stock_transfer,
    search_stock_transfers,
    approve_stock_transfer,
    reject_stock_transfer,
    mark_stock_transfer_in_transit,
    complete_stock_transfer,
    cancel_stock_transfer,
)

from app.stock_transfers.constants import (
    READ_ROLES,
    MANAGEMENT_ROLES,
    APPROVAL_ROLES,
    EXECUTION_ROLES,
)

router = APIRouter()


# -------------------------------------------------
# Search
# -------------------------------------------------


@router.post(
    "/search",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def search(
    request: StockTransferSearchRequest,
    db: Session = Depends(get_db),
):
    return search_stock_transfers(
        db,
        request,
    )


# -------------------------------------------------
# Get
# -------------------------------------------------


@router.get(
    "/{stock_transfer_id}",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def get(
    stock_transfer_id: int,
    db: Session = Depends(get_db),
):
    return get_stock_transfer(
        db,
        stock_transfer_id,
    )


# -------------------------------------------------
# Create
# -------------------------------------------------


@router.post("/")
def create(
    request: StockTransferCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(*MANAGEMENT_ROLES),
    ),
):
    return create_stock_transfer(
        db,
        request,
        current_user["user_id"],
    )


# -------------------------------------------------
# Update
# -------------------------------------------------


@router.put(
    "/{stock_transfer_id}",
)
def update(
    stock_transfer_id: int,
    request: StockTransferUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(*MANAGEMENT_ROLES),
    ),
):
    return update_stock_transfer(
        db,
        stock_transfer_id,
        request,
        current_user["user_id"],
    )


# -------------------------------------------------
# Approve
# -------------------------------------------------


@router.patch(
    "/{stock_transfer_id}/approve",
)
def approve(
    stock_transfer_id: int,
    request: StockTransferApproveRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(*APPROVAL_ROLES),
    ),
):
    return approve_stock_transfer(
        db,
        stock_transfer_id,
        current_user["user_id"],
    )


# -------------------------------------------------
# Reject
# -------------------------------------------------


@router.patch(
    "/{stock_transfer_id}/reject",
)
def reject(
    stock_transfer_id: int,
    request: StockTransferRejectRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(*APPROVAL_ROLES),
    ),
):
    return reject_stock_transfer(
        db,
        stock_transfer_id,
        current_user["user_id"],
    )


# -------------------------------------------------
# Move to In Transit
# -------------------------------------------------


@router.patch(
    "/{stock_transfer_id}/in-transit",
)
def in_transit(
    stock_transfer_id: int,
    request: StockTransferTransitRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(*EXECUTION_ROLES),
    ),
):
    return mark_stock_transfer_in_transit(
        db,
        stock_transfer_id,
        current_user["user_id"],
    )


# -------------------------------------------------
# Complete
# -------------------------------------------------


@router.patch(
    "/{stock_transfer_id}/complete",
)
def complete(
    stock_transfer_id: int,
    request: StockTransferCompleteRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(*EXECUTION_ROLES),
    ),
):
    return complete_stock_transfer(
        db,
        stock_transfer_id,
        current_user["user_id"],
    )


# -------------------------------------------------
# Cancel
# -------------------------------------------------


@router.patch(
    "/{stock_transfer_id}/cancel",
)
def cancel(
    stock_transfer_id: int,
    request: StockTransferCancelRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(*MANAGEMENT_ROLES),
    ),
):
    return cancel_stock_transfer(
        db,
        stock_transfer_id,
        current_user["user_id"],
    )
