from pydantic import BaseModel
from datetime import datetime

from app.common.pagination import PaginationRequest


class SubCategoryCreateRequest(BaseModel):
    name: str
    category_id: int


class SubCategoryUpdateRequest(BaseModel):
    name: str
    category_id: int


class SubCategoryResponse(BaseModel):
    id: int
    name: str

    category_id: int
    category_name: str

    is_active: bool

    created_by: int
    updated_by: int | None

    created_at: datetime
    updated_at: datetime | None


class SubCategorySearchRequest(PaginationRequest):
    category_id: int | None = None
    is_active: bool | None = None
