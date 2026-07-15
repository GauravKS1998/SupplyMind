from pydantic import BaseModel
from datetime import datetime

from app.common.pagination import PaginationRequest


class ProductTypeCreateRequest(BaseModel):
    name: str
    subcategory_id: int


class ProductTypeUpdateRequest(BaseModel):
    name: str
    subcategory_id: int


class ProductTypeResponse(BaseModel):
    id: int
    name: str

    subcategory_id: int
    subcategory_name: str

    is_active: bool

    created_by: int
    updated_by: int | None

    created_at: datetime
    updated_at: datetime | None


class ProductTypeSearchRequest(PaginationRequest):
    subcategory_id: int | None = None
    is_active: bool | None = None
