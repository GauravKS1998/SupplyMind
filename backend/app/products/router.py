from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from .service import (
    get_all_products,
    create_product,
    get_product_by_id,
    update_product,
    delete_product,
)

from .schema import ProductCreateRequest, ProductUpdateRequest

router = APIRouter()


# Depends is equivalent to @Autowired
@router.get("/")
def get_products(
    db: Session = Depends(get_db),  # means: FastAPI, give me a database session.
):
    return get_all_products(db)


@router.get("/{product_id}")
def get_single_product(
    product_id: int,  # Similar to @PathVariable Integer id
    db: Session = Depends(get_db),
):
    return get_product_by_id(db, product_id)


@router.post("/")
def add_product(request: ProductCreateRequest, db: Session = Depends(get_db)):
    return create_product(db, request)


@router.put("/{product_id}")
def update_existing_product(
    product_id: int, request: ProductUpdateRequest, db: Session = Depends(get_db)
):
    return update_product(db, product_id, request)


@router.delete("/{product_id}")
def remove_product(product_id: int, db: Session = Depends(get_db)):
    return delete_product(db, product_id)
