from datetime import datetime, timezone
from math import ceil

from sqlalchemy.orm import Session

from app.common.pagination import PaginationMeta
from app.common.responses import PaginatedResponse
from app.logging.logger import logger

from app.common.entity_utils import get_or_raise

from .exceptions import (
    UnitOfMeasureAlreadyExistsException,
    UnitOfMeasureInactiveException,
    UnitOfMeasureNotFoundException,
)

from .mapper import (
    map_unit_of_measure,
    map_units_of_measure,
)

from .model import UnitOfMeasure

from .repository import (
    find_by_code,
    find_by_id,
    find_by_name,
    find_units_of_measure,
    save,
)

from .schema import (
    UnitOfMeasureCreateRequest,
    UnitOfMeasureSearchRequest,
    UnitOfMeasureUpdateRequest,
)


def search_units_of_measure(
    db: Session,
    request: UnitOfMeasureSearchRequest,
):
    units, total_items = find_units_of_measure(
        db=db,
        page=request.page,
        size=request.size,
        search=request.search,
        is_active=request.is_active,
        sort_by=request.sort_by,
        direction=request.direction,
    )

    total_pages = ceil(total_items / request.size) if total_items > 0 else 0

    pagination = PaginationMeta(
        page=request.page,
        size=request.size,
        total_items=total_items,
        total_pages=total_pages,
        has_next=request.page < total_pages,
        has_previous=request.page > 1,
    )

    return PaginatedResponse(
        items=map_units_of_measure(units),
        pagination=pagination,
    )


def get_unit_of_measure_by_id(
    db: Session,
    uom_id: int,
):
    uom = get_or_raise(
        find_by_id(db, uom_id),
        UnitOfMeasureNotFoundException("Unit of Measure not found"),
    )

    return map_unit_of_measure(uom)


def create_unit_of_measure(
    db: Session,
    request: UnitOfMeasureCreateRequest,
    current_user_id: int,
):
    existing_name = find_by_name(
        db,
        request.name,
    )

    if existing_name:
        raise UnitOfMeasureAlreadyExistsException("Unit of Measure name already exists")

    existing_code = find_by_code(
        db,
        request.code,
    )

    if existing_code:
        raise UnitOfMeasureAlreadyExistsException("Unit of Measure code already exists")

    uom = UnitOfMeasure(
        name=request.name.strip(),
        code=request.code.strip().upper(),
        is_active=True,
        created_by=current_user_id,
    )

    saved_uom = save(
        db,
        uom,
    )

    db.commit()
    db.refresh(saved_uom)

    logger.info(f"Unit of Measure {saved_uom.id} created")

    return map_unit_of_measure(saved_uom)


def update_unit_of_measure(
    db: Session,
    uom_id: int,
    request: UnitOfMeasureUpdateRequest,
    current_user_id: int,
):
    uom = get_or_raise(
        find_by_id(db, uom_id),
        UnitOfMeasureNotFoundException("Unit of Measure not found"),
    )

    if not uom.is_active:
        raise UnitOfMeasureInactiveException("Unit of Measure is inactive")

    existing_name = find_by_name(
        db,
        request.name,
    )

    if existing_name and existing_name.id != uom.id:
        raise UnitOfMeasureAlreadyExistsException("Unit of Measure name already exists")

    existing_code = find_by_code(
        db,
        request.code,
    )

    if existing_code and existing_code.id != uom.id:
        raise UnitOfMeasureAlreadyExistsException("Unit of Measure code already exists")

    uom.name = request.name.strip()
    uom.code = request.code.strip().upper()

    uom.updated_by = current_user_id
    uom.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(uom)

    logger.info(f"Unit of Measure {uom.id} updated")

    return map_unit_of_measure(uom)


def deactivate_unit_of_measure(
    db: Session,
    uom_id: int,
    current_user_id: int,
):
    uom = get_or_raise(
        find_by_id(db, uom_id),
        UnitOfMeasureNotFoundException("Unit of Measure not found"),
    )

    if not uom.is_active:
        return {"message": "Unit of Measure already inactive"}

    uom.is_active = False
    uom.deactivated_by = current_user_id
    uom.updated_by = current_user_id
    uom.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(uom)

    logger.info(f"Unit of Measure {uom.id} deactivated")

    return {"message": "Unit of Measure deactivated successfully"}


def reactivate_unit_of_measure(
    db: Session,
    uom_id: int,
    current_user_id: int,
):
    uom = get_or_raise(
        find_by_id(db, uom_id),
        UnitOfMeasureNotFoundException("Unit of Measure not found"),
    )

    if uom.is_active:
        return {"message": "Unit of Measure already active"}

    uom.is_active = True
    uom.reactivated_by = current_user_id
    uom.updated_by = current_user_id
    uom.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(uom)

    logger.info(f"Unit of Measure {uom.id} reactivated")

    return {"message": "Unit of Measure reactivated successfully"}
