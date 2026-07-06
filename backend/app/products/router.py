from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.auth.dependencies import require_roles
from app.auth.enums import UserRole
from app.database.database import get_db

from .service import (
    get_all_products,
    get_active_products,
    get_inactive_products,
    get_product_by_id,
    get_products_by_supplier_id,
    get_products_by_category_id,
    get_products_by_subcategory_id,
    get_products_by_product_type_id,
    create_product,
    update_product,
    deactivate_product,
    reactivate_product,
)

from .schema import ProductCreateRequest, ProductUpdateRequest

router = APIRouter()


# Depends is equivalent to @Autowired
@router.get(
    "/",
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
def get_products(
    db: Session = Depends(get_db),  # means: FastAPI, give me a database session.
):
    return get_all_products(db)


@router.get(
    "/active",
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
def get_active(db: Session = Depends(get_db)):
    return get_active_products(db)


@router.get(
    "/inactive",
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
def get_inactive(db: Session = Depends(get_db)):
    return get_inactive_products(db)


@router.get(
    "/supplier/{supplier_id}",
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
def get_product_by_supplier(supplier_id: int, db: Session = Depends(get_db)):
    return get_products_by_supplier_id(db, supplier_id)


@router.get(
    "/category/{category_id}",
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
def get_product_by_category(category_id: int, db: Session = Depends(get_db)):
    return get_products_by_category_id(db, category_id)


@router.get(
    "/subcategory/{subcategory_id}",
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
def get_product_by_subcategory(subcategory_id: int, db: Session = Depends(get_db)):
    return get_products_by_subcategory_id(db, subcategory_id)


@router.get(
    "/product-type/{product_type_id}",
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
def get_product_by_product_type(product_type_id: int, db: Session = Depends(get_db)):
    return get_products_by_product_type_id(db, product_type_id)


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
