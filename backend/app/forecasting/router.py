from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from .service import forecast_product_demand

router = APIRouter()


@router.get("/{product_id}")
def forecast(product_id: int, db: Session = Depends(get_db)):
    return forecast_product_demand(db, product_id)
