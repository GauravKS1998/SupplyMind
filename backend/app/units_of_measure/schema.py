from datetime import datetime

from pydantic import BaseModel

from app.common.pagination import PaginationRequest


class UnitOfMeasureCreateRequest(BaseModel):
    name: str
    code: str


class UnitOfMeasureUpdateRequest(BaseModel):
    name: str
    code: str


class UnitOfMeasureResponse(BaseModel):
    id: int

    name: str
    code: str

    is_active: bool

    created_by: int
    updated_by: int | None
    deactivated_by: int | None
    reactivated_by: int | None

    created_at: datetime
    updated_at: datetime | None


class UnitOfMeasureSearchRequest(PaginationRequest):
    is_active: bool | None = None
