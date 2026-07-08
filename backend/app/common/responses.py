from typing import Generic, TypeVar

from pydantic import BaseModel

from .pagination import PaginationMeta

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):

    items: list[T]

    pagination: PaginationMeta
