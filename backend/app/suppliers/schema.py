from pydantic import BaseModel, EmailStr

from .enums import SupplierType


class SupplierCreateRequest(BaseModel):
    user_id: int
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
    supplier_type: SupplierType
    lead_time_days: int
    payment_terms: str
    rating: float
    is_verified: bool
    is_active: bool
