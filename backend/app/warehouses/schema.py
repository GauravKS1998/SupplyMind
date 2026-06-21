from pydantic import BaseModel
from datetime import datetime


class WarehouseCreateRequest(BaseModel):
    name: str
    location: str
    capacity: int


class WarehouseUpdateRequest(BaseModel):
    name: str
    location: str
    capacity: int


class WarehouseResponse(BaseModel):
    id: int
    name: str
    location: str
    capacity: int
    created_at: datetime
