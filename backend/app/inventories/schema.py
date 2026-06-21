from pydantic import BaseModel

from datetime import datetime


class InventoryCreateRequest(BaseModel):
    product_id: int
    warehouse_id: int
    quantity: int
    reorder_level: int


class InventoryUpdateRequest(BaseModel):
    quantity: int
    reorder_level: int


class InventoryResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    warehouse_id: int
    warehouse_name: str
    quantity: int
    reorder_level: int
    created_at: datetime
