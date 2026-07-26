from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.common.pagination import PaginationRequest
from .enums import PurchaseOrderStatus


class PurchaseOrderLineCreateRequest(BaseModel):
    product_id: int

    ordered_quantity: int

    unit_price: Decimal
    discount_amount: Decimal = Decimal("0.00")
    tax_amount: Decimal = Decimal("0.00")

    remarks: str | None = None


class PurchaseOrderLineUpdateRequest(BaseModel):
    id: int | None = None
    product_id: int

    ordered_quantity: int

    unit_price: Decimal
    discount_amount: Decimal = Decimal("0.00")
    tax_amount: Decimal = Decimal("0.00")

    remarks: str | None = None


class PurchaseOrderCreateRequest(BaseModel):
    supplier_id: int

    warehouse_id: int

    expected_delivery_date: datetime | None = None

    remarks: str | None = None

    lines: list[PurchaseOrderLineCreateRequest]


class PurchaseOrderUpdateRequest(BaseModel):
    supplier_id: int
    warehouse_id: int
    expected_delivery_date: datetime | None = None
    remarks: str | None = None

    lines: list[PurchaseOrderLineUpdateRequest]

    deleted_line_ids: list[int] = []


class PurchaseOrderRejectRequest(BaseModel):
    remarks: str


class PurchaseOrderCancelRequest(BaseModel):
    remarks: str


class SupplierSummary(BaseModel):
    id: int
    supplier_code: str
    supplier_name: str


class WarehouseSummary(BaseModel):
    id: int
    warehouse_code: str
    warehouse_name: str


class UomSummary(BaseModel):
    id: int
    code: str
    name: str


class ProductSummary(BaseModel):
    id: int
    sku: str
    name: str
    uom: UomSummary


class PurchaseOrderLineResponse(BaseModel):
    id: int

    line_number: int

    product: ProductSummary

    product_name_snapshot: str
    product_sku_snapshot: str

    ordered_quantity: int
    received_quantity: int

    unit_price: Decimal
    discount_amount: Decimal
    tax_amount: Decimal
    line_total: Decimal

    remarks: str | None = None


class PurchaseOrderResponse(BaseModel):
    id: int

    po_number: str

    supplier: SupplierSummary

    warehouse: WarehouseSummary

    status: PurchaseOrderStatus

    expected_delivery_date: datetime | None = None

    subtotal: Decimal
    discount_total: Decimal
    tax_total: Decimal
    grand_total: Decimal

    remarks: str | None = None

    created_at: datetime
    updated_at: datetime

    lines: list[PurchaseOrderLineResponse]


class PurchaseOrderSearchRequest(PaginationRequest):
    po_number: str | None = None

    supplier_id: int | None = None

    warehouse_id: int | None = None

    status: PurchaseOrderStatus | None = None

    expected_delivery_from: datetime | None = None
    expected_delivery_to: datetime | None = None

    created_from: datetime | None = None
    created_to: datetime | None = None
