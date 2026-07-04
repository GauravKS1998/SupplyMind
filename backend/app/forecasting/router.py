from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from .service import (
    forecast_product_demand,
    forecast_by_supplier,
    forecast_by_category,
    forecast_by_subcategory,
    forecast_by_product_type,
)

router = APIRouter()


@router.get("/{product_id}")
def forecast(product_id: int, db: Session = Depends(get_db)):
    return forecast_product_demand(db, product_id)


@router.get("/supplier/{supplier_id}")
def supplier_forecast(supplier_id: int, db: Session = Depends(get_db)):
    return forecast_by_supplier(db, supplier_id)


@router.get("/category/{category_id}")
def category_forecast(category_id: int, db: Session = Depends(get_db)):
    return forecast_by_category(db, category_id)


@router.get("/subcategory/{subcategory_id}")
def subcategory_forecast(subcategory_id: int, db: Session = Depends(get_db)):
    return forecast_by_subcategory(db, subcategory_id)


@router.get("/product_type/{product_type_id}")
def product_type_forecast(product_type_id: int, db: Session = Depends(get_db)):
    return forecast_by_product_type(db, product_type_id)
