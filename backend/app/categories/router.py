from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.auth.dependencies import require_roles
from app.auth.enums import UserRole
from app.database.database import get_db

from .service import (
    search_categories,
    get_all_categories,
    get_active_categories,
    get_inactive_categories,
    create_category,
    update_category,
    deactivate_category,
    reactivate_category,
)

from .schema import CategoryCreateRequest, CategoryUpdateRequest, CategorySearchRequest

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


@router.post("/search", dependencies=[Depends(require_roles(*READ_ROLES))])
def search_category_list(request: CategorySearchRequest, db: Session = Depends(get_db)):
    return search_categories(db, request)


@router.get(
    "/",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def get_categories(db: Session = Depends(get_db)):
    return get_all_categories(db)


@router.get(
    "/active",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def get_active(db: Session = Depends(get_db)):
    return get_active_categories(db)


@router.get(
    "/inactive",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def get_inactive(db: Session = Depends(get_db)):
    return get_inactive_categories(db)


@router.post("/")
def add_category(
    request: CategoryCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*WRITE_ROLES)),
):
    return create_category(db, request, current_user["user_id"])


@router.put("/{category_id}")
def update_existing_category(
    category_id: int,
    request: CategoryUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*WRITE_ROLES)),
):
    return update_category(db, category_id, request, current_user["user_id"])


@router.put("/{category_id}/deactivate")
def deactivate(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*WRITE_ROLES)),
):
    return deactivate_category(db, category_id, current_user["user_id"])


@router.put("/{category_id}/reactivate")
def deactivate(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*WRITE_ROLES)),
):
    return reactivate_category(db, category_id, current_user["user_id"])
