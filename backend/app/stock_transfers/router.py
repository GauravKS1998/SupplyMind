from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

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
def initiate(request: StockTransferRequest, db: Session = Depends(get_db)):
    return initiate_transfer(db, request)


@router.put("/{transfer_id}/approve/{approver_id}")
def approve(transfer_id: int, approver_id: int, db: Session = Depends(get_db)):
    return approve_transfer(db, transfer_id, approver_id)


@router.put("/{transfer_id}/reject")
def reject(transfer_id: int, db: Session = Depends(get_db)):
    return reject_transfer(db, transfer_id)


@router.put("/{transfer_id}/in-transit")
def move_to_transit(transfer_id: int, db: Session = Depends(get_db)):
    return mark_in_transit(db, transfer_id)


@router.put("/{transfer_id}/complete")
def complete(transfer_id: int, db: Session = Depends(get_db)):
    return complete_transfer(db, transfer_id)


@router.put("/{transfer_id}/cancel")
def cancel(transfer_id: int, db: Session = Depends(get_db)):
    return cancel_transfer(db, transfer_id)
