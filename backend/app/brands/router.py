from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.auth.dependencies import require_roles

from app.users.enums import UserRole

from .schema import (
    BrandCreateRequest,
    BrandSearchRequest,
    BrandUpdateRequest,
)

from .service import (
    get_brand_by_id,
    create_brand,
    update_brand,
    deactivate_brand,
    search_brands,
    reactivate_brand,
)

router = APIRouter()

READ_ROLES = (
    UserRole.ADMIN,
    UserRole.SUPER_ADMIN,
    UserRole.PROCUREMENT_MANAGER,
    UserRole.WAREHOUSE_MANAGER,
    UserRole.WAREHOUSE_STAFF,
    UserRole.SALES_MANAGER,
    UserRole.INVENTORY_ANALYST,
)

WRITE_ROLES = (
    UserRole.ADMIN,
    UserRole.SUPER_ADMIN,
    UserRole.PROCUREMENT_MANAGER,
)


@router.post(
    "/search",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def search(
    request: BrandSearchRequest,
    db: Session = Depends(get_db),
):
    return search_brands(
        db,
        request,
    )


@router.get(
    "/{brand_id}",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def get_single_brand(
    brand_id: int,
    db: Session = Depends(get_db),
):
    return get_brand_by_id(db, brand_id)


@router.post("/")
def add_brand(
    request: BrandCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*WRITE_ROLES)),
):
    return create_brand(
        db,
        request,
        current_user["user_id"],
    )


@router.put("/{brand_id}")
def update_existing_brand(
    brand_id: int,
    request: BrandUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*WRITE_ROLES)),
):
    return update_brand(
        db,
        brand_id,
        request,
        current_user["user_id"],
    )


@router.put("/{brand_id}/deactivate")
def deactivate_existing_brand(
    brand_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*WRITE_ROLES)),
):
    return deactivate_brand(
        db,
        brand_id,
        current_user["user_id"],
    )


@router.put("/{brand_id}/reactivate")
def reactivate_existing_brand(
    brand_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*WRITE_ROLES)),
):
    return reactivate_brand(
        db,
        brand_id,
        current_user["user_id"],
    )
