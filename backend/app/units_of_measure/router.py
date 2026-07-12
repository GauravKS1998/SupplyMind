from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from app.auth.dependencies import require_roles
from app.auth.enums import UserRole
from app.database.database import get_db

from .schema import (
    UnitOfMeasureCreateRequest,
    UnitOfMeasureSearchRequest,
    UnitOfMeasureUpdateRequest,
)

from .service import (
    create_unit_of_measure,
    deactivate_unit_of_measure,
    get_unit_of_measure_by_id,
    reactivate_unit_of_measure,
    search_units_of_measure,
    update_unit_of_measure,
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
    request: UnitOfMeasureSearchRequest,
    db: Session = Depends(get_db),
):
    return search_units_of_measure(
        db,
        request,
    )


@router.get(
    "/{uom_id}",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def get_single_unit_of_measure(
    uom_id: int,
    db: Session = Depends(get_db),
):
    return get_unit_of_measure_by_id(
        db,
        uom_id,
    )


@router.post("/")
def add_unit_of_measure(
    request: UnitOfMeasureCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*WRITE_ROLES)),
):
    return create_unit_of_measure(
        db,
        request,
        current_user["user_id"],
    )


@router.put("/{uom_id}")
def update_existing_unit_of_measure(
    uom_id: int,
    request: UnitOfMeasureUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*WRITE_ROLES)),
):
    return update_unit_of_measure(
        db,
        uom_id,
        request,
        current_user["user_id"],
    )


@router.put("/{uom_id}/deactivate")
def deactivate_existing_unit_of_measure(
    uom_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*WRITE_ROLES)),
):
    return deactivate_unit_of_measure(
        db,
        uom_id,
        current_user["user_id"],
    )


@router.put("/{uom_id}/reactivate")
def reactivate_existing_unit_of_measure(
    uom_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*WRITE_ROLES)),
):
    return reactivate_unit_of_measure(
        db,
        uom_id,
        current_user["user_id"],
    )
