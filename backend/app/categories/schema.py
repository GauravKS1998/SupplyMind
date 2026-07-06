from pydantic import BaseModel
from datetime import datetime


class CategoryCreateRequest(BaseModel):
    name: str


class CategoryUpdateRequest(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    id: int
    name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime | None
