from pydantic import BaseModel

from .enums import WarehouseType


class WarehouseCreateRequest(BaseModel):
    warehouse_code: str
    name: str
    warehouse_type: WarehouseType
    manager_id: int
    capacity: float
    address: str
    city: str
    state: str
    country: str
    postal_code: str


class WarehouseUpdateRequest(BaseModel):
    name: str
    warehouse_type: WarehouseType
    manager_id: int
    capacity: float
    address: str
    city: str
    state: str
    country: str
    postal_code: str


class WarehouseResponse(BaseModel):
    id: int
    warehouse_code: str
    name: str
    warehouse_type: WarehouseType
    manager_id: int
    capacity: float
    current_utilization: float
    is_active: bool
    created_by: int
    updated_by: int | None
