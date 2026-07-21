from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from app.auth.dependencies import require_roles
from app.users.enums import UserRole
from app.database.database import get_db

from .schema import (
    SupplierCreateRequest,
    SupplierUpdateRequest,
    SupplierSearchRequest,
)

from .service import (
    create_supplier,
    update_supplier,
    verify_supplier,
    get_supplier_by_id,
    get_supplier_by_user_id,
    get_all_suppliers,
    get_pending_suppliers,
    deactivate_supplier,
    reactivate_supplier,
    get_active_suppliers,
    get_inactive_suppliers,
    search_suppliers,
)

router = APIRouter()


# -------------------------
# Create
# -------------------------


@router.post("/")
def create(
    request: SupplierCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.SUPPLIER)),
):
    return create_supplier(
        db,
        request,
        current_user["user_id"],
    )


# -------------------------
# Search
# -------------------------


@router.post(
    "/search",
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
def search(
    request: SupplierSearchRequest,
    db: Session = Depends(get_db),
):
    return search_suppliers(
        db,
        request,
    )


# -------------------------
# All
# -------------------------


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
def get_all(
    db: Session = Depends(get_db),
):
    return get_all_suppliers(db)


# -------------------------
# Active
# -------------------------


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
def get_active(
    db: Session = Depends(get_db),
):
    return get_active_suppliers(db)


# -------------------------
# Inactive
# -------------------------


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
def get_inactive(
    db: Session = Depends(get_db),
):
    return get_inactive_suppliers(db)


# -------------------------
# Pending Verification
# -------------------------


@router.get("/pending")
def get_pending(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
            UserRole.PROCUREMENT_MANAGER,
        )
    ),
):
    return get_pending_suppliers(db)


# -------------------------
# Current Supplier Profile
# -------------------------


@router.get("/me")
def get_my_supplier_profile(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.SUPPLIER)),
):
    return get_supplier_by_user_id(
        db,
        current_user["user_id"],
    )


# -------------------------
# Get By ID
# -------------------------


@router.get(
    "/{supplier_id}",
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
    supplier_id: int,
    db: Session = Depends(get_db),
):
    return get_supplier_by_id(
        db,
        supplier_id,
    )


# -------------------------
# Update
# -------------------------


@router.put("/{supplier_id}")
def update(
    supplier_id: int,
    request: SupplierUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(UserRole.SUPPLIER)),
):
    return update_supplier(
        db,
        supplier_id,
        request,
        current_user["user_id"],
    )


# -------------------------
# Verify
# -------------------------


@router.put("/{supplier_id}/verify")
def verify(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
            UserRole.PROCUREMENT_MANAGER,
        )
    ),
):
    return verify_supplier(
        db,
        supplier_id,
        current_user["user_id"],
    )


# -------------------------
# Deactivate
# -------------------------


@router.put("/{supplier_id}/deactivate")
def deactivate(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
        )
    ),
):
    return deactivate_supplier(
        db,
        supplier_id,
        current_user["user_id"],
    )


# -------------------------
# Reactivate
# -------------------------


@router.put("/{supplier_id}/reactivate")
def reactivate(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.SUPER_ADMIN,
        )
    ),
):
    return reactivate_supplier(
        db,
        supplier_id,
        current_user["user_id"],
    )
