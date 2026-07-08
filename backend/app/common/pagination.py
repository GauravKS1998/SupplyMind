from pydantic import BaseModel, Field

from .constants import (
    DEFAULT_PAGE,
    DEFAULT_PAGE_SIZE,
    MAX_PAGE_SIZE,
    ASC,
)


class PaginationRequest(BaseModel):

    page: int = Field(default=DEFAULT_PAGE, ge=1)

    size: int = Field(
        default=DEFAULT_PAGE_SIZE,
        ge=1,
        le=MAX_PAGE_SIZE,
    )

    sort_by: str | None = None

    direction: str = ASC

    search: str | None = None


class PaginationMeta(BaseModel):

    page: int

    size: int

    total_items: int

    total_pages: int

    has_next: bool

    has_previous: bool
