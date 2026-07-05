from pydantic import BaseModel
from datetime import datetime


class CustomerCreateRequest(BaseModel):
    user_id: int
    company_name: str
    gst_number: str | None = None
    contact_person: str
    phone: str
    address: str
    city: str
    state: str
    country: str
    pincode: str


class CustomerUpdateRequest(BaseModel):
    company_name: str
    gst_number: str | None = None
    contact_person: str
    phone: str
    address: str
    city: str
    state: str
    country: str
    pincode: str


class CustomerResponse(BaseModel):
    id: int
    user_id: int
    company_name: str
    gst_number: str | None
    contact_person: str
    phone: str
    address: str
    city: str
    state: str
    country: str
    pincode: str
    is_verified: bool
    is_active: bool
    created_at: datetime
