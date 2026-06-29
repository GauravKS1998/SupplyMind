from pydantic import BaseModel
from datetime import datetime


class PurchaseOrderCreateRequest(BaseModel):
    supplier_id: int
    product_id: int
    warehouse_id: int
    quantity: int


class PurchaseOrderResponse(BaseModel):
    id: int
    supplier_id: int
    product_id: int
    warehouse_id: int
    quantity: int
    status: str
    ordered_at: datetime
