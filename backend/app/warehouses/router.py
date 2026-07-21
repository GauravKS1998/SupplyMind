from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.auth.dependencies import require_roles
from app.users.enums import UserRole
from app.database.database import get_db

from .schema import (
    WarehouseCreateRequest,
    WarehouseUpdateRequest,
    WarehouseSearchRequest,
)

from .service import (
    search_warehouses,
    get_all_warehouses,
    get_warehouse_by_id,
    create_warehouse,
    update_warehouse,
    deactivate_warehouse,
    reactivate_warehouse,
    get_active_warehouses,
    get_inactive_warehouses,
)

router = APIRouter()

READ_ROLES = (
    UserRole.ADMIN,
    UserRole.SUPER_ADMIN,
    UserRole.WAREHOUSE_MANAGER,
    UserRole.WAREHOUSE_STAFF,
    UserRole.INVENTORY_ANALYST,
)


@router.post(
    "/search",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def search(
    request: WarehouseSearchRequest,
    db: Session = Depends(get_db),
):
    return search_warehouses(
        db,
        request,
    )


@router.get(
    "/",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def get_all(
    db: Session = Depends(get_db),
):
    return get_all_warehouses(db)


@router.get(
    "/active",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def get_active(db: Session = Depends(get_db)):
    return get_active_warehouses(db)


@router.get(
    "/inactive",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def get_inactive(db: Session = Depends(get_db)):
    return get_inactive_warehouses(db)


@router.get(
    "/{warehouse_id}",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def get_single_warehouse(
    warehouse_id: int,
    db: Session = Depends(get_db),
):
    return get_warehouse_by_id(db, warehouse_id)


@router.post("/")
def create(
    request: WarehouseCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.WAREHOUSE_MANAGER)
    ),
):
    return create_warehouse(db, request, current_user["user_id"])


@router.put("/{warehouse_id}")
def update(
    warehouse_id: int,
    request: WarehouseUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.WAREHOUSE_MANAGER)
    ),
):
    return update_warehouse(db, warehouse_id, request, current_user["user_id"])


@router.put("/{warehouse_id}/deactivate")
def deactivate(
    warehouse_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.ADMIN, UserRole.SUPER_ADMIN)),
):
    return deactivate_warehouse(db, warehouse_id, current_user["user_id"])


@router.put("/{warehouse_id}/reactivate")
def reactivate(
    warehouse_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.ADMIN, UserRole.SUPER_ADMIN)),
):
    return reactivate_warehouse(db, warehouse_id, current_user["user_id"])
