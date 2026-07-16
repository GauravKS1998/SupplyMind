from pydantic import BaseModel
from datetime import datetime

from app.common.pagination import PaginationRequest

from .enums import WarehouseType


class WarehouseCreateRequest(BaseModel):
    warehouse_code: str
    name: str
    description: str | None
    warehouse_type: WarehouseType

    manager_user_id: int

    capacity: float

    address: str
    city: str
    state: str
    country: str
    postal_code: str


class WarehouseUpdateRequest(BaseModel):
    name: str
    description: str | None
    warehouse_type: WarehouseType

    manager_user_id: int

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
    description: str | None
    warehouse_type: WarehouseType

    manager_user_id: int

    capacity: float
    current_utilization: float

    address: str
    city: str
    state: str
    country: str
    postal_code: str

    is_active: bool

    created_by: int
    updated_by: int | None

    deactivated_by: int | None
    reactivated_by: int | None

    created_at: datetime
    updated_at: datetime | None


class WarehouseSearchRequest(PaginationRequest):

    warehouse_type: WarehouseType | None = None

    city: str | None = None

    state: str | None = None

    country: str | None = None

    is_active: bool | None = None
