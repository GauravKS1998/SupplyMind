from pydantic import BaseModel
from datetime import datetime

from app.common.pagination import PaginationRequest


class CategoryCreateRequest(BaseModel):
    name: str


class CategoryUpdateRequest(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    id: int
    name: str
    is_active: bool

    created_by: int
    updated_by: int | None

    created_at: datetime
    updated_at: datetime | None


class CategorySearchRequest(PaginationRequest):
    is_active: bool | None = None
