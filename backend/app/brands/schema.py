from pydantic import BaseModel
from datetime import datetime


class BrandCreateRequest(BaseModel):
    name: str
    description: str | None = None


class BrandUpdateRequest(BaseModel):
    name: str
    description: str | None = None


class BrandResponse(BaseModel):
    id: int
    name: str
    description: str | None

    is_active: bool

    created_by: int
    updated_by: int | None
    deactivated_by: int | None
    reactivated_by: int | None

    created_at: datetime
    updated_at: datetime | None
