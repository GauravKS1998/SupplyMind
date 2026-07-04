from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from .service import (
    get_all_subcategories,
    get_all_subcategories_by_category,
    create_subcategory,
)

from .schema import SubCategoryCreateRequest

router = APIRouter()


@router.get("/")
def get_subcategories(db: Session = Depends(get_db)):
    return get_all_subcategories(db)


@router.get("/{category_id}")
def get_subcategories_by_category(category_id: int, db: Session = Depends(get_db)):
    return get_all_subcategories_by_category(db, category_id)


@router.post("/")
def add_subcategory(request: SubCategoryCreateRequest, db: Session = Depends(get_db)):
    return create_subcategory(db, request)
