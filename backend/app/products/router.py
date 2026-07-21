from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.auth.dependencies import require_roles
from app.users.enums import UserRole
from app.database.database import get_db

from .service import (
    get_product_by_id,
    search_products,
    create_product,
    update_product,
    deactivate_product,
    reactivate_product,
)

from .schema import ProductCreateRequest, ProductUpdateRequest, ProductSearchRequest

router = APIRouter()


@router.post(
    "/search",
    dependencies=[
        Depends(
            require_roles(
                UserRole.ADMIN,
                UserRole.SUPER_ADMIN,
                UserRole.PROCUREMENT_MANAGER,
                UserRole.WAREHOUSE_MANAGER,
                UserRole.WAREHOUSE_STAFF,
                UserRole.SALES_MANAGER,
                UserRole.INVENTORY_ANALYST,
            )
        )
    ],
)
def search(
    request: ProductSearchRequest,
    db: Session = Depends(get_db),
):
    return search_products(db, request)


# Depends is equivalent to @Autowired
@router.get(
    "/{product_id}",
    dependencies=[
        Depends(
            require_roles(
                UserRole.ADMIN,
                UserRole.SUPER_ADMIN,
                UserRole.PROCUREMENT_MANAGER,
                UserRole.WAREHOUSE_MANAGER,
                UserRole.WAREHOUSE_STAFF,
                UserRole.SALES_MANAGER,
                UserRole.INVENTORY_ANALYST,
            )
        )
    ],
)
def get_single_product(
    product_id: int,  # Similar to @PathVariable Integer id
    db: Session = Depends(get_db),
):
    return get_product_by_id(db, product_id)


@router.post("/")
def add_product(
    request: ProductCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.PROCUREMENT_MANAGER
        )
    ),
):
    return create_product(db, request, current_user["user_id"])


@router.put("/{product_id}")
def update_existing_product(
    product_id: int,
    request: ProductUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.PROCUREMENT_MANAGER
        )
    ),
):
    return update_product(db, product_id, request, current_user["user_id"])


@router.put("/{product_id}/deactivate")
def deactivate_existing_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.PROCUREMENT_MANAGER
        )
    ),
):
    return deactivate_product(db, product_id, current_user["user_id"])


@router.put("/{product_id}/reactivate")
def reactivate_existing_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.PROCUREMENT_MANAGER
        )
    ),
):
    return reactivate_product(db, product_id, current_user["user_id"])
