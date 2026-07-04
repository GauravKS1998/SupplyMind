from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from .service import (
    get_all_categories,
    create_category,
    get_category_by_id,
    update_category,
    delete_category,
)

from .schema import CategoryCreateRequest, CategoryUpdateRequest

router = APIRouter()


@router.get("/")
def get_categories(db: Session = Depends(get_db)):
    return get_all_categories(db)


@router.get("/{category_id}")
def get_single_category(category_id: int, db: Session = Depends(get_db)):
    return get_category_by_id(db, category_id)


@router.post("/")
def add_category(request: CategoryCreateRequest, db: Session = Depends(get_db)):
    return create_category(db, request)


@router.put("/{category_id}")
def update_existing_category(
    category_id: int, request: CategoryUpdateRequest, db: Session = Depends(get_db)
):
    return update_category(db, category_id, request)


@router.delete("/{category_id}")
def remove_category(category_id: int, db: Session = Depends(get_db)):
    return delete_category(db, category_id)
