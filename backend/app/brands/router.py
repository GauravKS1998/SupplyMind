from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.auth.dependencies import require_roles

from app.auth.enums import UserRole

from .schema import (
    BrandCreateRequest,
    BrandUpdateRequest,
)

from .service import (
    get_all_brands,
    get_active_brands,
    get_inactive_brands,
    get_brand_by_id,
    create_brand,
    update_brand,
    deactivate_brand,
    reactivate_brand,
)

router = APIRouter()


@router.get(
    "/",
    dependencies=[
        Depends(
            require_roles(
                UserRole.ADMIN,
                UserRole.SUPER_ADMIN,
                UserRole.PROCUREMENT_MANAGER,
                UserRole.INVENTORY_ANALYST,
            )
        )
    ],
)
def get_all(db: Session = Depends(get_db)):
    return get_all_brands(db)


@router.get(
    "/active",
    dependencies=[
        Depends(
            require_roles(
                UserRole.ADMIN,
                UserRole.SUPER_ADMIN,
                UserRole.PROCUREMENT_MANAGER,
                UserRole.INVENTORY_ANALYST,
            )
        )
    ],
)
def get_active(db: Session = Depends(get_db)):
    return get_active_brands(db)


@router.get(
    "/inactive",
    dependencies=[
        Depends(
            require_roles(
                UserRole.ADMIN,
                UserRole.SUPER_ADMIN,
                UserRole.PROCUREMENT_MANAGER,
                UserRole.INVENTORY_ANALYST,
            )
        )
    ],
)
def get_inactive(db: Session = Depends(get_db)):
    return get_inactive_brands(db)


@router.get(
    "/{brand_id}",
    dependencies=[
        Depends(
            require_roles(
                UserRole.ADMIN,
                UserRole.SUPER_ADMIN,
                UserRole.PROCUREMENT_MANAGER,
                UserRole.INVENTORY_ANALYST,
            )
        )
    ],
)
def get_by_id(
    brand_id: int,
    db: Session = Depends(get_db),
):
    return get_brand_by_id(db, brand_id)


@router.post("/")
def create(
    request: BrandCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
            UserRole.PROCUREMENT_MANAGER,
        )
    ),
):
    return create_brand(
        db,
        request,
        current_user["user_id"],
    )


@router.put("/{brand_id}")
def update(
    brand_id: int,
    request: BrandUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
            UserRole.PROCUREMENT_MANAGER,
        )
    ),
):
    return update_brand(
        db,
        brand_id,
        request,
        current_user["user_id"],
    )


@router.put("/{brand_id}/deactivate")
def deactivate(
    brand_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
        )
    ),
):
    return deactivate_brand(
        db,
        brand_id,
        current_user["user_id"],
    )


@router.put("/{brand_id}/reactivate")
def reactivate(
    brand_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
        )
    ),
):
    return reactivate_brand(
        db,
        brand_id,
        current_user["user_id"],
    )
