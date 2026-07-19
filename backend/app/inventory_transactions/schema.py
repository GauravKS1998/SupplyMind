from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.common.pagination import PaginationRequest

from .enums import InventoryTransactionType, InventoryReferenceType


class InventoryTransactionResponse(BaseModel):
    id: int
    inventory_id: int

    transaction_type: InventoryTransactionType

    quantity_before: int
    quantity_delta: int
    quantity_after: int

    reserved_quantity_before: int
    reserved_quantity_after: int

    available_quantity_before: int
    available_quantity_after: int

    reason: str | None = None

    reference_type: InventoryReferenceType | None = None
    reference_id: int | None = None

    created_by: int
    created_at: datetime


class InventoryTransactionSearchRequest(PaginationRequest):
    inventory_id: Optional[int] | None = None

    transaction_type: InventoryTransactionType | None = None
    reference_type: InventoryReferenceType | None = None
    reference_id: Optional[int] | None = None

    created_by: Optional[int] | None = None
