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

router = APIRouter()


@router.post("/")
def create(request: PurchaseOrderCreateRequest, db: Session = Depends(get_db)):
    return create_draft_po(db, request)


@router.put("/{po_id}/submit")
def submit(po_id: int, db: Session = Depends(get_db)):
    return submit_po(db, po_id)


@router.put("/{po_id}/approve/{approver_id}")
def approve(po_id: int, approver_id: int, db: Session = Depends(get_db)):
    return approve_po(db, po_id, approver_id)


@router.put("/{po_id}/reject")
def reject(po_id: int, db: Session = Depends(get_db)):
    return reject_po(db, po_id)


@router.put("/{po_id}/ordered")
def ordered(po_id: int, db: Session = Depends(get_db)):
    return mark_ordered(db, po_id)


@router.put("/{po_id}/in-transit")
def in_transit(po_id: int, db: Session = Depends(get_db)):
    return mark_in_transit(db, po_id)


@router.put("/{po_id}/receive")
def receive(po_id: int, db: Session = Depends(get_db)):
    return receive_po(db, po_id)


@router.put("/{po_id}/close")
def close(po_id: int, db: Session = Depends(get_db)):
    return close_po(db, po_id)


@router.put("/{po_id}/cancel")
def cancel(po_id: int, db: Session = Depends(get_db)):
    return cancel_po(db, po_id)
