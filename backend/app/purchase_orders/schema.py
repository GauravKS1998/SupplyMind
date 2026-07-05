from pydantic import BaseModel
from datetime import datetime

from .enums import PurchaseOrderStatus


class PurchaseOrderCreateRequest(BaseModel):
    po_number: str
    supplier_id: int
    product_id: int
    warehouse_id: int
    quantity: int
    expected_delivery_date: datetime | None = None


class PurchaseOrderResponse(BaseModel):
    id: int
    po_number: str
    supplier_id: int
    supplier_name: str
    product_id: int
    product_name: str
    product_sku: str
    warehouse_id: int
    warehouse_name: str
    quantity: int
    status: PurchaseOrderStatus
    expected_delivery_date: datetime | None
    actual_delivery_date: datetime | None
    created_by: int
    approved_by: int | None
    closed_by: int | None
    cancelled_by: int | None
    rejected_by: int | None
    updated_by: int | None
    updated_at: datetime | None
    created_at: datetime
