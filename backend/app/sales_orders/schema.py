from pydantic import BaseModel
from datetime import datetime


class SalesOrderCreateRequest(BaseModel):
    product_id: int
    warehouse_id: int
    quantity: int


class SalesOrderResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_sku: str
    warehouse_id: int
    warehouse_name: str
    quantity: int
    total_price: float
    sold_at: datetime
