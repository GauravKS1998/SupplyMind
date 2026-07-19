from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.auth.dependencies import require_roles
from app.auth.enums import UserRole
from app.database.database import get_db

from .service import (
    search_inventories,
    get_all_inventories,
    get_inventory_by_id,
    create_inventory,
    update_inventory,
    deactivate_inventory,
    reactivate_inventory,
    get_active_inventories,
    get_inactive_inventories,
    increase_inventory,
    decrease_inventory,
    reserve_inventory,
    release_inventory,
    adjust_inventory,
)

from .schema import (
    InventoryCreateRequest,
    InventoryUpdateRequest,
    InventorySearchRequest,
    InventoryIncreaseRequest,
    InventoryDecreaseRequest,
    InventoryReserveRequest,
    InventoryReleaseRequest,
    InventoryAdjustRequest,
)

router = APIRouter()

READ_ROLES = (
    UserRole.ADMIN,
    UserRole.SUPER_ADMIN,
    UserRole.WAREHOUSE_MANAGER,
    UserRole.WAREHOUSE_STAFF,
    UserRole.PROCUREMENT_MANAGER,
    UserRole.SALES_MANAGER,
    UserRole.INVENTORY_ANALYST,
)

WRITE_ROLES = (
    UserRole.WAREHOUSE_MANAGER,
    UserRole.SUPER_ADMIN,
    UserRole.ADMIN,
)


@router.post(
    "/search",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def search(
    request: InventorySearchRequest,
    db: Session = Depends(get_db),
):
    return search_inventories(
        db,
        request,
    )


@router.get(
    "/",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def get_inventories(db: Session = Depends(get_db)):
    return get_all_inventories(db)


@router.get(
    "/active",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def get_active(
    db: Session = Depends(get_db),
):
    return get_active_inventories(db)


@router.get(
    "/inactive",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def get_inactive(
    db: Session = Depends(get_db),
):
    return get_inactive_inventories(db)


@router.get(
    "/{inventory_id}",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def get_single_inventory(
    inventory_id: int,
    db: Session = Depends(get_db),
):
    return get_inventory_by_id(
        db,
        inventory_id,
    )


@router.post("/")
def add_inventory(
    request: InventoryCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*WRITE_ROLES)),
):
    return create_inventory(db, request, current_user["user_id"])


@router.put("/{inventory_id}")
def update(
    inventory_id: int,
    request: InventoryUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*WRITE_ROLES)),
):
    return update_inventory(db, inventory_id, request, current_user["user_id"])


@router.put("/{inventory_id}/deactivate")
def deactivate(
    inventory_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*WRITE_ROLES)),
):
    return deactivate_inventory(db, inventory_id, current_user["user_id"])


@router.put("/{inventory_id}/reactivate")
def reactivate(
    inventory_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*WRITE_ROLES)),
):
    return reactivate_inventory(db, inventory_id, current_user["user_id"])


@router.post(
    "/{inventory_id}/increase",
)
def increase(
    inventory_id: int,
    request: InventoryIncreaseRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*WRITE_ROLES)),
):
    return increase_inventory(
        db,
        inventory_id,
        request,
        current_user["user_id"],
    )


@router.post(
    "/{inventory_id}/decrease",
)
def decrease_inventory_endpoint(
    inventory_id: int,
    request: InventoryDecreaseRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*WRITE_ROLES)),
):
    return decrease_inventory(
        db=db,
        inventory_id=inventory_id,
        request=request,
        current_user_id=current_user["user_id"],
    )


@router.post(
    "/{inventory_id}/reserve",
)
def reserve_inventory_endpoint(
    inventory_id: int,
    request: InventoryReserveRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*WRITE_ROLES)),
):
    return reserve_inventory(
        db=db,
        inventory_id=inventory_id,
        request=request,
        current_user_id=current_user["user_id"],
    )


@router.post(
    "/{inventory_id}/release",
)
def release_inventory_endpoint(
    inventory_id: int,
    request: InventoryReleaseRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*WRITE_ROLES)),
):
    return release_inventory(
        db=db,
        inventory_id=inventory_id,
        request=request,
        current_user_id=current_user["user_id"],
    )


@router.post(
    "/{inventory_id}/adjust",
)
def adjust_inventory_endpoint(
    inventory_id: int,
    request: InventoryAdjustRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*WRITE_ROLES)),
):
    return adjust_inventory(
        db=db,
        inventory_id=inventory_id,
        request=request,
        current_user_id=current_user["user_id"],
    )
