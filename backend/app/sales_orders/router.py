from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import require_roles
from app.database.database import get_db

from app.sales_orders.schema import (
    SalesOrderCancelRequest,
    SalesOrderCompleteRequest,
    SalesOrderConfirmRequest,
    SalesOrderCreateRequest,
    SalesOrderDeliverRequest,
    SalesOrderDispatchRequest,
    SalesOrderReserveRequest,
    SalesOrderReturnRequest,
    SalesOrderSearchRequest,
    SalesOrderUpdateRequest,
)

from app.sales_orders.service import (
    cancel_sales_order,
    complete_sales_order,
    confirm_sales_order,
    create_sales_order,
    deliver_sales_order,
    dispatch_sales_order,
    get_sales_order,
    return_sales_order,
    search_sales_orders,
    reserve_sales_order,
    update_sales_order,
)

from app.sales_orders.constants import (
    READ_ROLES,
    APPROVAL_ROLES,
    MANAGEMENT_ROLES,
    RESERVATION_ROLES,
    DELIVERY_ROLES,
    CUSTOMER_ROLES,
)

router = APIRouter()


@router.post(
    "/search",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def search(
    request: SalesOrderSearchRequest,
    db: Session = Depends(get_db),
):
    return search_sales_orders(
        db,
        request,
    )


@router.get(
    "/{sales_order_id}",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def get(
    sales_order_id: int,
    db: Session = Depends(get_db),
):
    return get_sales_order(
        db,
        sales_order_id,
    )


@router.post("/")
def create(
    request: SalesOrderCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(*MANAGEMENT_ROLES),
    ),
):
    return create_sales_order(
        db,
        request,
        current_user["user_id"],
    )


@router.put("/{sales_order_id}")
def update(
    sales_order_id: int,
    request: SalesOrderUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(*MANAGEMENT_ROLES),
    ),
):
    return update_sales_order(
        db,
        sales_order_id,
        request,
        current_user["user_id"],
    )


@router.patch(
    "/{sales_order_id}/confirm",
)
def confirm(
    sales_order_id: int,
    request: SalesOrderConfirmRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(*APPROVAL_ROLES),
    ),
):
    return confirm_sales_order(
        db,
        sales_order_id,
        current_user["user_id"],
    )


@router.patch(
    "/{sales_order_id}/reserve",
)
def reserve(
    sales_order_id: int,
    request: SalesOrderReserveRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(*RESERVATION_ROLES),
    ),
):
    return reserve_sales_order(
        db,
        sales_order_id,
        current_user["user_id"],
    )


@router.patch(
    "/{sales_order_id}/dispatch",
)
def dispatch(
    sales_order_id: int,
    request: SalesOrderDispatchRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(*DELIVERY_ROLES),
    ),
):
    return dispatch_sales_order(
        db,
        sales_order_id,
        current_user["user_id"],
    )


@router.patch(
    "/{sales_order_id}/deliver",
)
def deliver(
    sales_order_id: int,
    request: SalesOrderDeliverRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(*DELIVERY_ROLES),
    ),
):
    return deliver_sales_order(
        db,
        sales_order_id,
        current_user["user_id"],
    )


@router.patch(
    "/{sales_order_id}/complete",
)
def complete(
    sales_order_id: int,
    request: SalesOrderCompleteRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(*APPROVAL_ROLES),
    ),
):
    return complete_sales_order(
        db,
        sales_order_id,
        current_user["user_id"],
    )


@router.patch(
    "/{sales_order_id}/cancel",
)
def cancel(
    sales_order_id: int,
    request: SalesOrderCancelRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(*MANAGEMENT_ROLES),
    ),
):
    return cancel_sales_order(
        db,
        sales_order_id,
        current_user["user_id"],
    )


@router.patch(
    "/{sales_order_id}/return",
)
def return_order(
    sales_order_id: int,
    request: SalesOrderReturnRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(*CUSTOMER_ROLES),
    ),
):
    return return_sales_order(
        db,
        sales_order_id,
        current_user["user_id"],
    )
