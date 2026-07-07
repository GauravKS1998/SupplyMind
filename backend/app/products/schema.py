from pydantic import BaseModel
from datetime import datetime


class ProductCreateRequest(BaseModel):
    name: str
    description: str | None = None
    sku: str
    barcode: str | None = None

    supplier_id: int
    category_id: int
    subcategory_id: int
    product_type_id: int

    brand_id: int
    uom_id: int

    purchase_price: float
    selling_price: float


class ProductUpdateRequest(BaseModel):
    name: str
    description: str | None = None
    sku: str
    barcode: str | None = None

    supplier_id: int
    category_id: int
    subcategory_id: int
    product_type_id: int

    brand_id: int
    uom_id: int

    purchase_price: float
    selling_price: float


class ProductResponse(BaseModel):
    id: int

    name: str
    description: str | None
    sku: str
    barcode: str | None

    supplier_id: int
    supplier_name: str

    category_id: int
    category_name: str

    subcategory_id: int
    subcategory_name: str

    product_type_id: int
    product_type_name: str

    brand_id: int
    brand_name: str

    uom_id: int
    uom_code: str
    uom_name: str

    purchase_price: float
    selling_price: float

    is_active: bool

    created_by: int
    updated_by: int | None

    deactivated_by: int | None
    reactivated_by: int | None

    created_at: datetime
    updated_at: datetime | None
