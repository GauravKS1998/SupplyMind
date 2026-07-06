from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.auth.dependencies import require_roles
from app.auth.enums import UserRole
from app.database.database import get_db

from .service import (
    get_all_subcategories,
    get_active_subcategories,
    get_inactive_subcategories,
    get_all_subcategories_by_category,
    create_subcategory,
    update_subcategory,
    deactivate_subcategory,
    reactivate_subcategory,
)

from .schema import SubCategoryCreateRequest, SubCategoryUpdateRequest

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
def get_subcategories(db: Session = Depends(get_db)):
    return get_all_subcategories(db)


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
    return get_active_subcategories(db)


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
    return get_inactive_subcategories(db)


@router.get(
    "/{category_id}",
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
def get_subcategories_by_category(category_id: int, db: Session = Depends(get_db)):
    return get_all_subcategories_by_category(db, category_id)


@router.post("/")
def add_subcategory(
    request: SubCategoryCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.PROCUREMENT_MANAGER
        )
    ),
):
    return create_subcategory(db, request, current_user["user_id"])


@router.put("/{subcategory_id}")
def update_existing_subcategory(
    subcategory_id: int,
    request: SubCategoryUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.PROCUREMENT_MANAGER
        )
    ),
):
    return update_subcategory(db, subcategory_id, request, current_user["user_id"])


@router.put("/{subcategory_id}/deactivate")
def deactivate(
    subcategory_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.PROCUREMENT_MANAGER
        )
    ),
):
    return deactivate_subcategory(db, subcategory_id, current_user["user_id"])


@router.put("/{subcategory_id}/reactivate")
def deactivate(
    subcategory_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.PROCUREMENT_MANAGER
        )
    ),
):
    return reactivate_subcategory(db, subcategory_id, current_user["user_id"])
