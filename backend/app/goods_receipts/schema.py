from datetime import datetime

from pydantic import BaseModel

from app.common.pagination import PaginationRequest
from app.common.responses import PaginatedResponse

from app.purchase_orders.schema import ProductSummary
from app.purchase_orders.schema import WarehouseSummary

from .enums import GoodsReceiptStatus


class PurchaseOrderSummary(BaseModel):
    id: int
    po_number: str


# ---------------------------------------------------------------------
# Line Requests
# ---------------------------------------------------------------------


class GoodsReceiptLineCreateRequest(BaseModel):
    purchase_order_line_id: int
    product_id: int

    batch_number: str

    accepted_quantity: int
    rejected_quantity: int = 0

    remarks: str | None = None


class GoodsReceiptLineUpdateRequest(BaseModel):
    id: int | None = None

    purchase_order_line_id: int
    product_id: int

    batch_number: str

    accepted_quantity: int
    rejected_quantity: int = 0

    remarks: str | None = None


# ---------------------------------------------------------------------
# Header Requests
# ---------------------------------------------------------------------


class GoodsReceiptCreateRequest(BaseModel):
    purchase_order_id: int

    warehouse_id: int

    remarks: str | None = None

    lines: list[GoodsReceiptLineCreateRequest]


class GoodsReceiptUpdateRequest(BaseModel):
    purchase_order_id: int

    warehouse_id: int

    remarks: str | None = None

    lines: list[GoodsReceiptLineUpdateRequest]

    deleted_line_ids: list[int]


# ---------------------------------------------------------------------
# Responses
# ---------------------------------------------------------------------


class GoodsReceiptLineResponse(BaseModel):
    id: int

    line_number: int

    purchase_order_line_id: int

    product: ProductSummary

    batch_number: str

    accepted_quantity: int
    rejected_quantity: int

    remarks: str | None


class GoodsReceiptResponse(BaseModel):
    id: int

    grn_number: str

    purchase_order: PurchaseOrderSummary

    warehouse: WarehouseSummary

    status: GoodsReceiptStatus

    remarks: str | None

    created_by: int
    received_by: int | None
    approved_by: int | None
    cancelled_by: int | None
    updated_by: int | None

    created_at: datetime
    updated_at: datetime

    lines: list[GoodsReceiptLineResponse]


class GoodsReceiptSummaryResponse(BaseModel):
    id: int

    grn_number: str

    purchase_order: PurchaseOrderSummary

    warehouse: WarehouseSummary

    status: GoodsReceiptStatus

    created_at: datetime


# ---------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------


class GoodsReceiptSearchRequest(PaginationRequest):
    grn_number: str | None = None

    purchase_order_id: int | None = None

    warehouse_id: int | None = None

    status: GoodsReceiptStatus | None = None

    from_date: datetime | None = None

    to_date: datetime | None = None


# ---------------------------------------------------------------------
# Workflow Requests
# ---------------------------------------------------------------------


class GoodsReceiptSubmitRequest(BaseModel):
    remarks: str | None = None


class GoodsReceiptApproveRequest(BaseModel):
    remarks: str | None = None


class GoodsReceiptCancelRequest(BaseModel):
    remarks: str | None = None
