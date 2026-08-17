from datetime import datetime

from pydantic import BaseModel

from app.common.pagination import PaginationRequest

from app.purchase_orders.schema import (
    ProductSummary,
    WarehouseSummary,
)

from .enums import TransferStatus

# ---------------------------------------------------------------------
# Line Requests
# ---------------------------------------------------------------------


class StockTransferLineCreateRequest(BaseModel):
    product_id: int

    batch_number: str

    quantity: int

    remarks: str | None = None


class StockTransferLineUpdateRequest(BaseModel):
    id: int | None = None

    product_id: int

    batch_number: str

    quantity: int

    remarks: str | None = None


# ---------------------------------------------------------------------
# Header Requests
# ---------------------------------------------------------------------


class StockTransferCreateRequest(BaseModel):
    source_warehouse_id: int

    destination_warehouse_id: int

    remarks: str | None = None

    lines: list[StockTransferLineCreateRequest]


class StockTransferUpdateRequest(BaseModel):
    source_warehouse_id: int

    destination_warehouse_id: int

    remarks: str | None = None

    lines: list[StockTransferLineUpdateRequest]

    deleted_line_ids: list[int]


# ---------------------------------------------------------------------
# Responses
# ---------------------------------------------------------------------


class StockTransferLineResponse(BaseModel):
    id: int

    line_number: int

    product: ProductSummary

    product_name_snapshot: str
    product_sku_snapshot: str

    batch_number: str

    quantity: int

    remarks: str | None


class StockTransferResponse(BaseModel):
    id: int

    transfer_number: str

    source_warehouse: WarehouseSummary

    destination_warehouse: WarehouseSummary

    status: TransferStatus

    remarks: str | None

    initiated_by: int
    approved_by: int | None
    rejected_by: int | None
    cancelled_by: int | None
    completed_by: int | None
    updated_by: int | None

    created_at: datetime
    updated_at: datetime | None

    completed_at: datetime | None

    lines: list[StockTransferLineResponse]


# ---------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------


class StockTransferSearchRequest(PaginationRequest):
    transfer_number: str | None = None

    source_warehouse_id: int | None = None

    destination_warehouse_id: int | None = None

    status: TransferStatus | None = None

    created_from: datetime | None = None

    created_to: datetime | None = None


# ---------------------------------------------------------------------
# Workflow Requests
# ---------------------------------------------------------------------


class StockTransferApproveRequest(BaseModel):
    remarks: str | None = None


class StockTransferRejectRequest(BaseModel):
    remarks: str | None = None


class StockTransferTransitRequest(BaseModel):
    remarks: str | None = None


class StockTransferCompleteRequest(BaseModel):
    remarks: str | None = None


class StockTransferCancelRequest(BaseModel):
    remarks: str | None = None


# ---------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------


class StockTransferSummaryResponse(BaseModel):
    id: int

    transfer_number: str

    source_warehouse: WarehouseSummary

    destination_warehouse: WarehouseSummary

    status: TransferStatus

    created_at: datetime
