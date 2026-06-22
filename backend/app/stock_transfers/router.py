from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from .service import transfer_stock

from .schema import StockTransferRequest, StockTransferResponse

router = APIRouter()


@router.post("/")
def move_stock(request: StockTransferRequest, db: Session = Depends(get_db)):
    return transfer_stock(db, request)
