from pydantic import BaseModel

from datetime import datetime


class SupplierCreateRequest(BaseModel):
    name: str
    contact_email: str
    phone: str
    address: str


class SupplierUpdateRequest(BaseModel):
    name: str
    contact_email: str
    phone: str
    address: str


class SupplierResponse(BaseModel):
    id: int
    name: str
    contact_email: str
    phone: str
    address: str
    created_at: datetime
