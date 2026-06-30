from datetime import datetime, timezone
from typing import Optional, Generic, TypeVar, Any
from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int
    has_next: bool
    has_previous: bool


class StandardResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "Operation completed successfully"
    data: Optional[T] = None
    metadata: Optional[dict[str, Any]] = None
    errors: Optional[list[str]] = None
    request_id: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @staticmethod
    def ok(data: T = None, message: str = "Operation completed successfully",
           metadata: Optional[dict[str, Any]] = None, request_id: Optional[str] = None):
        return StandardResponse[T](
            success=True, message=message, data=data, metadata=metadata, request_id=request_id
        )

    @staticmethod
    def fail(message: str = "An error occurred", errors: Optional[list[str]] = None,
             request_id: Optional[str] = None):
        return StandardResponse(
            success=False, message=message, errors=errors, request_id=request_id
        )

    @staticmethod
    def paginated(data: T, pagination: Any, message: str = "Success",
                  request_id: Optional[str] = None):
        if hasattr(pagination, "model_dump"):
            meta = pagination.model_dump(exclude={"items"}, exclude_none=True)
        elif isinstance(pagination, dict):
            meta = pagination
        else:
            meta = {"note": "pagination unavailable"}
        return StandardResponse[T](
            success=True,
            message=message,
            data=data,
            metadata={"pagination": meta},
            request_id=request_id,
        )
