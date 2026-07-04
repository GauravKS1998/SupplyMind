from pydantic import BaseModel
from datetime import datetime


class SubCategoryCreateRequest(BaseModel):
    name: str
    category_id: int


class SubCategoryResponse(BaseModel):
    id: int
    name: str
    category_id: int
    category_name: str
    created_at: datetime
