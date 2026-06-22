from pydantic import BaseModel
from datetime import datetime


class StockTransferRequest(BaseModel):
    product_id: int
    source_warehouse_id: int
    destination_warehouse_id: int
    quantity: int


class StockTransferResponse(BaseModel):
    id: int
    product_id: int
    source_warehouse_id: int
    destination_warehouse_id: int
    quantity: int
    transferred_at: datetime
