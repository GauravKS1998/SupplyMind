from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.dependencies import require_roles

from app.goods_receipts.schema import (
    GoodsReceiptCreateRequest,
    GoodsReceiptUpdateRequest,
    GoodsReceiptSearchRequest,
)

from app.goods_receipts.service import (
    create_goods_receipt,
    update_goods_receipt,
    get_goods_receipt,
    search_goods_receipts,
    submit_goods_receipt,
    approve_goods_receipt,
    cancel_goods_receipt,
)

from app.goods_receipts.constants import (
    READ_ROLES,
    MANAGEMENT_ROLES,
    APPROVAL_ROLES,
)

router = APIRouter()


@router.post(
    "/search",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def search(
    request: GoodsReceiptSearchRequest,
    db: Session = Depends(get_db),
):
    return search_goods_receipts(
        db,
        request,
    )


@router.get(
    "/{goods_receipt_id}",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def get(
    goods_receipt_id: int,
    db: Session = Depends(get_db),
):
    return get_goods_receipt(
        db,
        goods_receipt_id,
    )


@router.post("/")
def create(
    request: GoodsReceiptCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*MANAGEMENT_ROLES)),
):
    return create_goods_receipt(
        db,
        request,
        current_user["user_id"],
    )


@router.put("/{goods_receipt_id}")
def update(
    goods_receipt_id: int,
    request: GoodsReceiptUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*MANAGEMENT_ROLES)),
):
    return update_goods_receipt(
        db,
        goods_receipt_id,
        request,
        current_user["user_id"],
    )


@router.patch(
    "/{goods_receipt_id}/submit",
)
def submit(
    goods_receipt_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*MANAGEMENT_ROLES)),
):
    return submit_goods_receipt(
        db,
        goods_receipt_id,
        current_user["user_id"],
    )


@router.patch(
    "/{goods_receipt_id}/approve",
)
def approve(
    goods_receipt_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*APPROVAL_ROLES)),
):
    return approve_goods_receipt(
        db,
        goods_receipt_id,
        current_user["user_id"],
    )


@router.patch(
    "/{goods_receipt_id}/cancel",
)
def cancel(
    goods_receipt_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*MANAGEMENT_ROLES)),
):
    return cancel_goods_receipt(
        db,
        goods_receipt_id,
        current_user["user_id"],
    )
