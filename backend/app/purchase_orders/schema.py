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
    supplier_name: str
    product_id: int
    product_name: str
    product_sku: str
    warehouse_id: int
    warehouse_name: str
    quantity: int
    status: str
    ordered_at: datetime
