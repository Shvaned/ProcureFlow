from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field


class BaseCreateDTO(BaseModel):
    pass


class BaseUpdateDTO(BaseModel):
    pass


class BaseResponseDTO(BaseModel):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class BaseFilterDTO(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    sort_field: Optional[str] = None
    sort_direction: Optional[str] = Field(default="asc", pattern="^(asc|desc)$")


class BasePaginationDTO(BaseModel):
    page: int = 1
    page_size: int = 20
    total: int = 0
    total_pages: int = 1
    has_next: bool = False
    has_previous: bool = False
