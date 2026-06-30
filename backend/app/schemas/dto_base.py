from datetime import datetime

from pydantic import BaseModel, Field


class BaseCreateDTO(BaseModel):
    pass


class BaseUpdateDTO(BaseModel):
    pass


class BaseResponseDTO(BaseModel):
    id: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


class BaseFilterDTO(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    sort_field: str | None = None
    sort_direction: str | None = Field(default="asc", pattern="^(asc|desc)$")


class BasePaginationDTO(BaseModel):
    page: int = 1
    page_size: int = 20
    total: int = 0
    total_pages: int = 1
    has_next: bool = False
    has_previous: bool = False
