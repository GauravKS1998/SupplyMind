from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.common.responses import PaginatedResponse

from app.auth.dependencies import require_roles

from app.auth.enums import UserRole

from .schema import (
    InventoryTransactionResponse,
    InventoryTransactionSearchRequest,
)

from .service import (
    get_transaction,
    search_transactions,
)

router = APIRouter()

# ---------------------------------------------------------
# Read Roles
# ---------------------------------------------------------

READ_ROLES = (
    UserRole.ADMIN,
    UserRole.SUPER_ADMIN,
    UserRole.WAREHOUSE_MANAGER,
    UserRole.WAREHOUSE_STAFF,
    UserRole.PROCUREMENT_MANAGER,
    UserRole.SALES_MANAGER,
    UserRole.INVENTORY_ANALYST,
)

# ---------------------------------------------------------
# Get Transaction By ID
# ---------------------------------------------------------


@router.get(
    "/{transaction_id}",
    response_model=InventoryTransactionResponse,
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def get_inventory_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
):
    return get_transaction(
        db,
        transaction_id,
    )


# ---------------------------------------------------------
# Search Transactions
# ---------------------------------------------------------


@router.post(
    "/search",
    response_model=PaginatedResponse[InventoryTransactionResponse],
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def search_inventory_transactions(
    request: InventoryTransactionSearchRequest,
    db: Session = Depends(get_db),
):
    return search_transactions(
        db,
        request,
    )


# ---------------------------------------------------------
# Get All Transactions
# ---------------------------------------------------------


@router.get(
    "",
    response_model=PaginatedResponse[InventoryTransactionResponse],
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def get_inventory_transactions(
    db: Session = Depends(get_db),
):
    return search_transactions(
        db,
        InventoryTransactionSearchRequest(),
    )
