from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.auth.dependencies import require_roles
from app.auth.enums import UserRole
from app.database.database import get_db

from .service import (
    search_product_types,
    get_all_product_types,
    get_active_product_types,
    get_inactive_product_types,
    get_all_product_types_by_subcategory,
    get_active_product_types_by_subcategory_id,
    create_product_type,
    update_product_type,
    deactivate_product_type,
    reactivate_product_type,
)

from .schema import (
    ProductTypeCreateRequest,
    ProductTypeUpdateRequest,
    ProductTypeSearchRequest,
)

router = APIRouter()

READ_ROLES = (
    UserRole.SUPER_ADMIN,
    UserRole.ADMIN,
    UserRole.PROCUREMENT_MANAGER,
    UserRole.WAREHOUSE_MANAGER,
    UserRole.WAREHOUSE_STAFF,
    UserRole.SALES_MANAGER,
    UserRole.FINANCE_MANAGER,
    UserRole.INVENTORY_ANALYST,
)

WRITE_ROLES = (UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.PROCUREMENT_MANAGER)


@router.post(
    "/search",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def search_product_type_list(
    request: ProductTypeSearchRequest,
    db: Session = Depends(get_db),
):
    return search_product_types(
        db,
        request,
    )


@router.get(
    "/",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def get_product_types(db: Session = Depends(get_db)):
    return get_all_product_types(db)


@router.get(
    "/active",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def get_active(db: Session = Depends(get_db)):
    return get_active_product_types(db)


@router.get(
    "/inactive",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def get_inactive(db: Session = Depends(get_db)):
    return get_inactive_product_types(db)


@router.get(
    "/subcategory/{subcategory_id}",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def get_product_types_by_subcategory(
    subcategory_id: int, db: Session = Depends(get_db)
):
    return get_all_product_types_by_subcategory(db, subcategory_id)


@router.get(
    "/subcategory/{subcategory_id}/active",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def get_active_product_types_by_subcategory(
    subcategory_id: int,
    db: Session = Depends(get_db),
):
    return get_active_product_types_by_subcategory_id(
        db,
        subcategory_id,
    )


@router.post("/")
def add_product_type(
    request: ProductTypeCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*WRITE_ROLES)),
):
    return create_product_type(db, request, current_user["user_id"])


@router.put("/{product_type_id}")
def update_existing_product_type(
    product_type_id: int,
    request: ProductTypeUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*WRITE_ROLES)),
):
    return update_product_type(db, product_type_id, request, current_user["user_id"])


@router.put("/{product_type_id}/deactivate")
def deactivate(
    product_type_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*WRITE_ROLES)),
):
    return deactivate_product_type(db, product_type_id, current_user["user_id"])


@router.put("/{product_type_id}/deactivate")
def reactivate(
    product_type_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*WRITE_ROLES)),
):
    return reactivate_product_type(db, product_type_id, current_user["user_id"])
