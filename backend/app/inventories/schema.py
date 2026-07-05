from pydantic import BaseModel
from datetime import date, datetime


class InventoryCreateRequest(BaseModel):
    product_id: int
    warehouse_id: int
    quantity: int
    reorder_level: int
    reorder_quantity: int
    batch_number: str
    expiry_date: date | None = None


class InventoryUpdateRequest(BaseModel):
    quantity: int
    reserved_quantity: int
    reorder_level: int
    reorder_quantity: int
    batch_number: str
    expiry_date: date | None = None


class InventoryResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_sku: str
    supplier_name: str
    category_name: str
    subcategory_name: str
    product_type_name: str
    warehouse_id: int
    warehouse_name: str
    quantity: int
    reserved_quantity: int
    available_quantity: int
    reorder_level: int
    reorder_quantity: int
    batch_number: str
    expiry_date: date | None
    last_stocked_at: datetime
    created_by: int
    updated_by: int | None
