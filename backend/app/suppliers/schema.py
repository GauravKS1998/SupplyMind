from pydantic import BaseModel, EmailStr

from app.common.pagination import PaginationRequest

from .enums import SupplierType


class SupplierCreateRequest(BaseModel):
    company_name: str

    gst_number: str | None = None

    contact_person: str
    phone: str
    email: EmailStr

    address: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None

    supplier_type: SupplierType | None = None

    lead_time_days: int | None = None
    payment_terms: str | None = None


class SupplierUpdateRequest(BaseModel):
    company_name: str | None = None

    gst_number: str | None = None

    contact_person: str | None = None
    phone: str | None = None
    email: EmailStr | None = None

    address: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None

    supplier_type: SupplierType | None = None

    lead_time_days: int | None = None
    payment_terms: str | None = None


class SupplierResponse(BaseModel):
    id: int
    user_id: int

    company_name: str

    gst_number: str | None

    contact_person: str
    phone: str
    email: str

    address: str | None
    city: str | None
    state: str | None
    country: str | None
    postal_code: str | None

    supplier_type: SupplierType | None

    lead_time_days: int | None
    payment_terms: str | None

    rating: float

    is_verified: bool
    is_active: bool

    profile_completion_percentage: int
    is_profile_complete: bool


class SupplierSearchRequest(PaginationRequest):
    supplier_type: SupplierType | None = None

    city: str | None = None
    state: str | None = None
    country: str | None = None

    is_verified: bool | None = None
    is_active: bool | None = None
