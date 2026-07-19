from pydantic import BaseModel
from datetime import date, datetime

from decimal import Decimal

from app.common.pagination import PaginationRequest

from app.inventory_transactions.enums import InventoryReferenceType


class InventoryCreateRequest(BaseModel):
    product_id: int
    warehouse_id: int

    quantity: int

    unit_cost: Decimal

    reorder_level: int
    reorder_quantity: int

    batch_number: str

    manufacturing_date: date | None = None
    expiry_date: date | None = None

    storage_location: str | None = None


class InventoryUpdateRequest(BaseModel):
    unit_cost: Decimal

    reorder_level: int
    reorder_quantity: int

    manufacturing_date: date | None = None
    expiry_date: date | None = None

    storage_location: str | None = None


class InventoryIncreaseRequest(BaseModel):
    quantity: int

    reason: str | None = None

    reference_type: InventoryReferenceType | None = None
    reference_id: int | None = None


class InventoryDecreaseRequest(BaseModel):
    quantity: int

    reason: str | None = None

    reference_type: InventoryReferenceType | None = None
    reference_id: int | None = None


class InventoryReserveRequest(BaseModel):
    quantity: int

    reason: str | None = None

    reference_type: InventoryReferenceType | None = None
    reference_id: int | None = None


class InventoryReleaseRequest(BaseModel):
    quantity: int

    reason: str | None = None

    reference_type: InventoryReferenceType | None = None
    reference_id: int | None = None


class InventoryAdjustRequest(BaseModel):
    quantity: int

    reason: str

    reference_type: InventoryReferenceType | None = None
    reference_id: int | None = None


class InventoryResponse(BaseModel):
    id: int

    product_id: int
    product_name: str
    product_sku: str

    supplier_id: int
    supplier_name: str

    category_id: int
    category_name: str

    subcategory_id: int
    subcategory_name: str

    product_type_id: int
    product_type_name: str

    warehouse_id: int
    warehouse_code: str
    warehouse_name: str

    quantity: int
    reserved_quantity: int
    available_quantity: int

    unit_cost: Decimal

    reorder_level: int
    reorder_quantity: int

    batch_number: str

    manufacturing_date: date | None
    expiry_date: date | None

    storage_location: str | None

    last_movement_at: datetime

    is_active: bool

    created_by: int
    updated_by: int | None

    deactivated_by: int | None
    reactivated_by: int | None

    created_at: datetime
    updated_at: datetime | None


class InventorySearchRequest(PaginationRequest):

    warehouse_id: int | None = None

    product_id: int | None = None

    batch_number: str | None = None

    is_active: bool | None = None

    expiry_before: date | None = None

    expiry_after: date | None = None

    manufacturing_before: date | None = None

    manufacturing_after: date | None = None

    low_stock_only: bool = False
