from pydantic import BaseModel
from datetime import datetime


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
    created_at: datetime
    updated_at: datetime | None
