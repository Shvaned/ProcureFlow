# ProcureFlow AI — Backend Infrastructure Guide

**Version:** 1.0.0
**Date:** 2026-06-30

---

## Overview

The backend follows Clean Architecture with strict layering. Every module (products, inventory, procurement, etc.) uses the same infrastructure pattern.

---

## Adding a New Module

### 1. Create Model in `app/models/{domain}/`

```python
from app.models.base import BaseEntity, SoftDeleteMixin, AuditMixin

class YourModel(BaseEntity, SoftDeleteMixin, AuditMixin):
    __tablename__ = "your_table"
    name: Mapped[str] = mapped_column(String(255), nullable=False)
```

### 2. Create Repository (reuse BaseRepository)

```python
from app.repositories.base import BaseRepository

class YourRepository(BaseRepository[YourModel]):
    model = YourModel
```

### 3. Create Service in `app/services/`

```python
from app.services.base import BaseService, UnitOfWork

class YourService(BaseService[YourModel]):
    def __init__(self, repository: YourRepository):
        self.repository = repository
```

### 4. Create DTOs in `app/schemas/`

```python
from app.schemas.dto_base import BaseCreateDTO, BaseResponseDTO

class YourCreateDTO(BaseCreateDTO):
    name: str

class YourResponseDTO(BaseResponseDTO):
    name: str
```

### 5. Create Controller in `app/api/`

```python
@router.get("/your-resource")
async def list_resource(
    _: User = Depends(RequirePermission("Your.Read")),
    db: AsyncSession = Depends(get_db),
):
    service = YourService(YourRepository(db))
    result = await service.find_all()
    return StandardResponse.ok(data=result)
```

### 6. Register in `app/api/router.py`

```python
from app.api.your_module import router as your_router
api_router.include_router(your_router, tags=["Your Module"])
```

---

## Base Classes Summary

| Class | Location | Purpose |
|-------|----------|---------|
| `BaseEntity` | `models/base.py` | Base + UUID + Timestamp |
| `SoftDeleteMixin` | `models/base.py` | deleted_at, is_deleted |
| `AuditMixin` | `models/base.py` | created_by, updated_by |
| `BaseRepository[T]` | `repositories/base.py` | Generic CRUD, filtering, pagination |
| `BaseService[T]` | `services/base.py` | Read-only operations |
| `CRUDService[T]` | `services/base.py` | Full CRUD |
| `UnitOfWork` | `services/base.py` | Transaction scope |
| `StandardResponse[T]` | `schemas/common.py` | Consistent API envelope |
| `BaseCreateDTO` | `schemas/dto_base.py` | Create DTO base |
| `BaseUpdateDTO` | `schemas/dto_base.py` | Update DTO base |
| `BaseResponseDTO` | `schemas/dto_base.py` | Response DTO base |
| `BaseFilterDTO` | `schemas/dto_base.py` | Filter DTO base |
| `BusinessValidator` | `core/validation.py` | Reusable validation methods |

---

## Exception Handling

All exceptions extend `ProcureFlowException` (in `core/exceptions.py`). The global handler in `core/exceptions_handlers.py` automatically maps them to HTTP responses. To add a new exception:

```python
class CustomException(ProcureFlowException):
    def __init__(self, message: str = "Custom error"):
        super().__init__(message, status_code=418)
```

---

## Filtering Engine

The `BaseRepository._apply_filters()` method supports 16 operators via `FilterCondition`:

`eq`, `neq`, `gt`, `gte`, `lt`, `lte`, `like`, `ilike`, `in`, `not_in`, `between`, `is_null`, `is_not_null`, `starts_with`, `ends_with`

Usage:
```python
filters = [
    FilterCondition(field="sku", operator="eq", value="ABC123"),
    FilterCondition(field="price", operator="gte", value=100),
]
result = await repository.find_all(filters=filters)
```

---

## AI Integration

AI features follow the strict governance model:
- AI receives structured context (never raw ORM objects or SQL)
- AI returns structured JSON validated against Pydantic schemas
- AI communicates through the `AIService` which wraps `OpenRouterProvider`
- All AI operations go through `explain_business_context()` or `generate_structured()`
- The `_try_ai_explain()` helper provides graceful degradation on AI failure

---

## Dependency Injection

FastAPI's `Depends()` is used throughout:
- `get_db()` — provides AsyncSession
- `get_current_user` — validates JWT + loads user with roles
- `RequirePermission("X.Read")` — RBAC enforcement
- Service/repository injection done manually in controller methods
