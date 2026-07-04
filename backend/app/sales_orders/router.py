from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from .service import create_sales_order, get_all_sales_orders

from .schema import SalesOrderCreateRequest

router = APIRouter()


@router.get("/")
def get_sales_orders(db: Session = Depends(get_db)):
    return get_all_sales_orders(db)


@router.post("/")
def add_sales_order(request: SalesOrderCreateRequest, db: Session = Depends(get_db)):
    return create_sales_order(db, request)
