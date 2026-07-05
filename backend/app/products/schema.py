from pydantic import BaseModel
from datetime import datetime


class ProductCreateRequest(BaseModel):
    name: str
    sku: str
    supplier_id: int
    category_id: int
    subcategory_id: int
    product_type_id: int
    price: float


class ProductUpdateRequest(BaseModel):
    name: str
    sku: str
    supplier_id: int
    category_id: int
    subcategory_id: int
    product_type_id: int
    price: float


class ProductResponse(BaseModel):
    id: int
    name: str
    sku: str
    supplier_id: int
    supplier_name: str
    category_id: int
    category_name: str
    subcategory_id: int
    subcategory_name: str
    product_type_id: int
    product_type_name: str
    price: float
    is_active: bool
    created_at: datetime
    updated_at: datetime | None
