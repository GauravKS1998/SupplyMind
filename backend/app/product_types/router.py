from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from .service import (
    get_all_product_types,
    get_all_product_types_by_subcategory,
    create_product_type,
)

from .schema import ProductTypeCreateRequest

router = APIRouter()


@router.get("/")
def get_product_types(db: Session = Depends(get_db)):
    return get_all_product_types(db)


@router.get("/{subcategory_id}")
def get_product_types_by_subcategory(
    subcategory_id: int, db: Session = Depends(get_db)
):
    return get_all_product_types_by_subcategory(db, subcategory_id)


@router.post("/")
def add_product_type(request: ProductTypeCreateRequest, db: Session = Depends(get_db)):
    return create_product_type(db, request)
