from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.common.pagination import PaginationRequest

# =========================================================
# Create
# =========================================================


class CustomerCreateRequest(BaseModel):
    company_name: str
    gst_number: str | None = None

    contact_person: str

    phone: str | None = None
    email: EmailStr | None = None

    address: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


# =========================================================
# Update
# =========================================================


class CustomerUpdateRequest(BaseModel):
    company_name: str
    gst_number: str | None = None

    contact_person: str

    phone: str | None = None
    email: EmailStr | None = None

    address: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


# =========================================================
# Response
# =========================================================


class CustomerResponse(BaseModel):
    id: int
    user_id: int

    company_name: str
    gst_number: str | None

    contact_person: str

    phone: str | None
    email: EmailStr | None

    address: str | None
    city: str | None
    state: str | None
    country: str | None
    postal_code: str | None

    is_verified: bool
    is_active: bool

    verified_by: int | None
    updated_by: int | None

    deactivated_by: int | None
    deactivated_at: datetime | None

    reactivated_by: int | None
    reactivated_at: datetime | None

    created_at: datetime
    updated_at: datetime


# =========================================================
# Search
# =========================================================


class CustomerSearchRequest(PaginationRequest):
    city: str | None = None
    state: str | None = None
    country: str | None = None

    is_verified: bool | None = None
    is_active: bool | None = None
