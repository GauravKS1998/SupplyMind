from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from .service import (
    get_all_purchase_orders,
    create_purchase_order,
    approve_purchase_order,
)

from .schema import PurchaseOrderCreateRequest

router = APIRouter()


@router.get("/")
def get_purchase_orders(db: Session = Depends(get_db)):
    return get_all_purchase_orders(db)


@router.post("/")
def add_purchase_order(
    request: PurchaseOrderCreateRequest, db: Session = Depends(get_db)
):
    return create_purchase_order(db, request)


@router.put("/{purchase_order_id}/approve")
def approve_order(purchase_order_id: int, db: Session = Depends(get_db)):
    return approve_purchase_order(db, purchase_order_id)
