from datetime import datetime, timezone

from sqlalchemy.orm import Session

from .model import Brand

from .schema import (
    BrandCreateRequest,
    BrandUpdateRequest,
    BrandResponse,
)

from .repository import (
    save,
    find_all,
    find_active,
    find_inactive,
    find_by_id,
    find_by_name,
)

from .exceptions import (
    BrandAlreadyExistsException,
    BrandNotFoundException,
    BrandInactiveException,
    BrandFailException,
)


def map_brand(brand: Brand):

    return BrandResponse(
        id=brand.id,
        name=brand.name,
        description=brand.description,
        is_active=brand.is_active,
        created_by=brand.created_by,
        updated_by=brand.updated_by,
        deactivated_by=brand.deactivated_by,
        reactivated_by=brand.reactivated_by,
        created_at=brand.created_at,
        updated_at=brand.updated_at,
    )


def get_all_brands(db: Session):

    brands = find_all(db)

    return [map_brand(b) for b in brands]


def get_active_brands(db: Session):

    brands = find_active(db)

    return [map_brand(b) for b in brands]


def get_inactive_brands(db: Session):

    brands = find_inactive(db)

    return [map_brand(b) for b in brands]


def get_brand_by_id(db: Session, brand_id: int):

    brand = find_by_id(db, brand_id)

    if not brand:
        raise BrandNotFoundException("Brand not found")

    return map_brand(brand)


def create_brand(
    db: Session,
    request: BrandCreateRequest,
    current_user_id: int,
):

    existing = find_by_name(db, request.name)

    if existing:
        raise BrandAlreadyExistsException("Brand already exists")

    brand = Brand(
        name=request.name,
        description=request.description,
        created_by=current_user_id,
        is_active=True,
    )

    saved = save(db, brand)

    return map_brand(saved)


def update_brand(
    db: Session,
    brand_id: int,
    request: BrandUpdateRequest,
    current_user_id: int,
):

    brand = find_by_id(db, brand_id)

    if not brand:
        raise BrandNotFoundException("Brand not found")

    if not brand.is_active:
        raise BrandInactiveException("Brand is inactive")

    existing = find_by_name(db, request.name)

    if existing and existing.id != brand.id:
        raise BrandAlreadyExistsException("Brand already exists")

    brand.name = request.name
    brand.description = request.description

    brand.updated_by = current_user_id
    brand.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(brand)

    return map_brand(brand)


def deactivate_brand(
    db: Session,
    brand_id: int,
    current_user_id: int,
):

    brand = find_by_id(db, brand_id)

    if not brand:
        raise BrandNotFoundException("Brand not found")

    if not brand.is_active:
        return {"message": "Brand already inactive"}

    brand.is_active = False

    brand.deactivated_by = current_user_id
    brand.updated_by = current_user_id
    brand.updated_at = datetime.now(timezone.utc)

    db.commit()

    return {"message": "Brand deactivated successfully"}


def reactivate_brand(
    db: Session,
    brand_id: int,
    current_user_id: int,
):

    brand = find_by_id(db, brand_id)

    if not brand:
        raise BrandNotFoundException("Brand not found")

    if brand.is_active:
        return {"message": "Brand already active"}

    brand.is_active = True

    brand.reactivated_by = current_user_id
    brand.updated_by = current_user_id
    brand.updated_at = datetime.now(timezone.utc)

    db.commit()

    return {"message": "Brand activated successfully"}
