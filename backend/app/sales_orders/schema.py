from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.common.pagination import PaginationRequest

from app.purchase_orders.schema import (
    ProductSummary,
    WarehouseSummary,
)

from .enums import SalesOrderStatus

# ---------------------------------------------------------------------
# Line Requests
# ---------------------------------------------------------------------


class SalesOrderLineCreateRequest(BaseModel):
    product_id: int

    ordered_quantity: int

    unit_price: Decimal
    discount_amount: Decimal = Decimal("0.00")
    tax_amount: Decimal = Decimal("0.00")

    remarks: str | None = None


class SalesOrderLineUpdateRequest(BaseModel):
    id: int | None = None

    product_id: int

    ordered_quantity: int

    unit_price: Decimal
    discount_amount: Decimal = Decimal("0.00")
    tax_amount: Decimal = Decimal("0.00")

    remarks: str | None = None


# ---------------------------------------------------------------------
# Header Requests
# ---------------------------------------------------------------------


class SalesOrderCreateRequest(BaseModel):
    customer_id: int

    warehouse_id: int

    remarks: str | None = None

    lines: list[SalesOrderLineCreateRequest]


class SalesOrderUpdateRequest(BaseModel):
    customer_id: int

    warehouse_id: int

    remarks: str | None = None

    lines: list[SalesOrderLineUpdateRequest]

    deleted_line_ids: list[int]


# ---------------------------------------------------------------------
# Responses
# ---------------------------------------------------------------------


class SalesOrderLineResponse(BaseModel):
    id: int

    line_number: int

    product: ProductSummary

    product_name_snapshot: str
    product_sku_snapshot: str

    ordered_quantity: int

    unit_price: Decimal
    discount_amount: Decimal
    tax_amount: Decimal
    line_total: Decimal

    remarks: str | None


class SalesOrderResponse(BaseModel):
    id: int

    so_number: str

    customer_id: int

    warehouse: WarehouseSummary

    status: SalesOrderStatus

    subtotal: Decimal
    discount_total: Decimal
    tax_total: Decimal
    grand_total: Decimal

    remarks: str | None

    created_by: int
    confirmed_by: int | None
    dispatched_by: int | None
    delivered_by: int | None
    completed_by: int | None
    cancelled_by: int | None
    returned_by: int | None
    updated_by: int | None

    created_at: datetime
    updated_at: datetime | None

    delivered_at: datetime | None
    completed_at: datetime | None
    returned_at: datetime | None

    lines: list[SalesOrderLineResponse]


# ---------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------


class SalesOrderSearchRequest(PaginationRequest):
    so_number: str | None = None

    customer_id: int | None = None

    warehouse_id: int | None = None

    status: SalesOrderStatus | None = None

    created_from: datetime | None = None
    created_to: datetime | None = None


# ---------------------------------------------------------------------
# Workflow Requests
# ---------------------------------------------------------------------


class SalesOrderConfirmRequest(BaseModel):
    remarks: str | None = None


class SalesOrderReserveRequest(BaseModel):
    remarks: str | None = None


class SalesOrderDispatchRequest(BaseModel):
    remarks: str | None = None


class SalesOrderDeliverRequest(BaseModel):
    remarks: str | None = None


class SalesOrderCompleteRequest(BaseModel):
    remarks: str | None = None


class SalesOrderCancelRequest(BaseModel):
    remarks: str | None = None


class SalesOrderReturnRequest(BaseModel):
    remarks: str | None = None


# ---------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------


class SalesOrderSummaryResponse(BaseModel):
    id: int

    so_number: str

    customer_id: int

    warehouse: WarehouseSummary

    status: SalesOrderStatus

    grand_total: Decimal

    created_at: datetime
