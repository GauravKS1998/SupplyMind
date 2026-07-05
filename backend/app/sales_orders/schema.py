from pydantic import BaseModel
from datetime import datetime

from .enums import SalesOrderStatus


class SalesOrderCreateRequest(BaseModel):
    so_number: str
    product_id: int
    warehouse_id: int
    customer_id: int
    quantity: int


class SalesOrderResponse(BaseModel):
    id: int
    so_number: str

    product_id: int
    product_name: str
    product_sku: str

    warehouse_id: int
    warehouse_name: str

    customer_id: int

    quantity: int
    total_price: float

    status: SalesOrderStatus

    created_by: int

    sold_at: datetime
