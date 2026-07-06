from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.auth.dependencies import require_roles
from app.auth.enums import UserRole
from app.database.database import get_db

from .service import (
    get_all_product_types,
    get_active_product_types,
    get_inactive_product_types,
    get_all_product_types_by_subcategory,
    create_product_type,
    update_product_type,
    deactivate_product_type,
    reactivate_product_type,
)

from .schema import ProductTypeCreateRequest, ProductTypeUpdateRequest

router = APIRouter()


@router.get(
    "/",
    dependencies=[
        Depends(
            require_roles(
                UserRole.SUPER_ADMIN,
                UserRole.ADMIN,
                UserRole.PROCUREMENT_MANAGER,
                UserRole.WAREHOUSE_MANAGER,
                UserRole.WAREHOUSE_STAFF,
                UserRole.SALES_MANAGER,
                UserRole.FINANCE_MANAGER,
                UserRole.INVENTORY_ANALYST,
            )
        )
    ],
)
def get_product_types(db: Session = Depends(get_db)):
    return get_all_product_types(db)


@router.get(
    "/active",
    dependencies=[
        Depends(
            require_roles(
                UserRole.SUPER_ADMIN,
                UserRole.ADMIN,
                UserRole.PROCUREMENT_MANAGER,
                UserRole.WAREHOUSE_MANAGER,
                UserRole.WAREHOUSE_STAFF,
                UserRole.SALES_MANAGER,
                UserRole.FINANCE_MANAGER,
                UserRole.INVENTORY_ANALYST,
            )
        )
    ],
)
def get_active(db: Session = Depends(get_db)):
    return get_active_product_types(db)


@router.get(
    "/inactive",
    dependencies=[
        Depends(
            require_roles(
                UserRole.SUPER_ADMIN,
                UserRole.ADMIN,
                UserRole.PROCUREMENT_MANAGER,
                UserRole.WAREHOUSE_MANAGER,
                UserRole.WAREHOUSE_STAFF,
                UserRole.SALES_MANAGER,
                UserRole.FINANCE_MANAGER,
                UserRole.INVENTORY_ANALYST,
            )
        )
    ],
)
def get_inactive(db: Session = Depends(get_db)):
    return get_inactive_product_types(db)


@router.get(
    "/{subcategory_id}",
    dependencies=[
        Depends(
            require_roles(
                UserRole.SUPER_ADMIN,
                UserRole.ADMIN,
                UserRole.PROCUREMENT_MANAGER,
                UserRole.WAREHOUSE_MANAGER,
                UserRole.WAREHOUSE_STAFF,
                UserRole.SALES_MANAGER,
                UserRole.FINANCE_MANAGER,
                UserRole.INVENTORY_ANALYST,
            )
        )
    ],
)
def get_product_types_by_subcategory(
    subcategory_id: int, db: Session = Depends(get_db)
):
    return get_all_product_types_by_subcategory(db, subcategory_id)


@router.post("/")
def add_product_type(
    request: ProductTypeCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.PROCUREMENT_MANAGER
        )
    ),
):
    return create_product_type(db, request, current_user["user_id"])


@router.put("/{product_type_id}")
def update_existing_product_type(
    product_type_id: int,
    request: ProductTypeUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.PROCUREMENT_MANAGER
        )
    ),
):
    return update_product_type(db, product_type_id, request, current_user["user_id"])


@router.put("/{product_type_id}/deactivate")
def deactivate(
    product_type_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.PROCUREMENT_MANAGER
        )
    ),
):
    return deactivate_product_type(db, product_type_id, current_user["user_id"])


@router.put("/{product_type_id}/deactivate")
def reactivate(
    product_type_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.PROCUREMENT_MANAGER
        )
    ),
):
    return reactivate_product_type(db, product_type_id, current_user["user_id"])
