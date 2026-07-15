from pydantic import BaseModel, EmailStr

from app.common.pagination import PaginationRequest

from .enums import SupplierType


class SupplierCreateRequest(BaseModel):
    company_name: str
    gst_number: str

    contact_person: str
    phone: str
    email: EmailStr

    address: str
    city: str
    state: str
    country: str
    postal_code: str

    supplier_type: SupplierType

    lead_time_days: int
    payment_terms: str


class SupplierUpdateRequest(BaseModel):
    company_name: str
    gst_number: str

    contact_person: str
    phone: str
    email: EmailStr

    address: str
    city: str
    state: str
    country: str
    postal_code: str

    supplier_type: SupplierType

    lead_time_days: int
    payment_terms: str


class SupplierResponse(BaseModel):
    id: int
    user_id: int

    company_name: str
    gst_number: str

    contact_person: str
    phone: str
    email: str

    address: str
    city: str
    state: str
    country: str
    postal_code: str

    supplier_type: SupplierType

    lead_time_days: int
    payment_terms: str

    rating: float

    is_verified: bool
    is_active: bool


class SupplierSearchRequest(PaginationRequest):
    supplier_type: SupplierType | None = None

    city: str | None = None
    state: str | None = None
    country: str | None = None

    is_verified: bool | None = None
    is_active: bool | None = None
