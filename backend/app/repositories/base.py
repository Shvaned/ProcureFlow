from typing import Any, Generic, Optional, TypeVar, Sequence, Callable
from uuid import UUID
from sqlalchemy import select, func, delete, update, and_, or_, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel

T = TypeVar("T", bound=DeclarativeBase)


class FilterOperator:
    EQ = "eq"
    NEQ = "neq"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    LIKE = "like"
    ILIKE = "ilike"
    IN = "in"
    NOT_IN = "not_in"
    BETWEEN = "between"
    IS_NULL = "is_null"
    IS_NOT_NULL = "is_not_null"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"


class FilterCondition(BaseModel):
    field: str
    operator: str
    value: Any = None


class SortParam(BaseModel):
    field: str
    direction: str = "asc"


class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 20


class PaginatedResult(BaseModel):
    items: list[Any]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool


class BaseRepository(Generic[T]):
    model: type[T]

    def __init__(self, db: AsyncSession):
        self.db = db

    def _apply_filters(self, stmt, filters: list[FilterCondition] | None):
        if not filters:
            return stmt
        for f in filters:
            column = getattr(self.model, f.field, None)
            if column is None:
                continue
            op = f.operator
            if op == FilterOperator.EQ:
                stmt = stmt.where(column == f.value)
            elif op == FilterOperator.NEQ:
                stmt = stmt.where(column != f.value)
            elif op == FilterOperator.GT:
                stmt = stmt.where(column > f.value)
            elif op == FilterOperator.GTE:
                stmt = stmt.where(column >= f.value)
            elif op == FilterOperator.LT:
                stmt = stmt.where(column < f.value)
            elif op == FilterOperator.LTE:
                stmt = stmt.where(column <= f.value)
            elif op == FilterOperator.ILIKE:
                stmt = stmt.where(column.ilike(f"%{f.value}%"))
            elif op == FilterOperator.LIKE:
                stmt = stmt.where(column.like(f"%{f.value}%"))
            elif op == FilterOperator.IN:
                stmt = stmt.where(column.in_(f.value))
            elif op == FilterOperator.NOT_IN:
                stmt = stmt.where(column.not_in(f.value))
            elif op == FilterOperator.BETWEEN:
                stmt = stmt.where(column.between(f.value[0], f.value[1]))
            elif op == FilterOperator.IS_NULL:
                stmt = stmt.where(column.is_(None))
            elif op == FilterOperator.IS_NOT_NULL:
                stmt = stmt.where(column.is_not(None))
            elif op == FilterOperator.STARTS_WITH:
                stmt = stmt.where(column.ilike(f"{f.value}%"))
            elif op == FilterOperator.ENDS_WITH:
                stmt = stmt.where(column.ilike(f"%{f.value}"))
        return stmt

    def _apply_sorting(self, stmt, sorting: list[SortParam] | None):
        if not sorting:
            return stmt
        for s in sorting:
            column = getattr(self.model, s.field, None)
            if column is None:
                continue
            stmt = stmt.order_by(column.desc() if s.direction == "desc" else column.asc())
        return stmt

    async def count(self, filters: list[FilterCondition] | None = None) -> int:
        stmt = select(func.count()).select_from(self.model)
        stmt = self._apply_filters(stmt, filters)
        result = await self.db.execute(stmt)
        return result.scalar_one()

    async def exists(self, id: UUID) -> bool:
        stmt = select(self.model).where(self.model.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def get_by_id(self, id: UUID) -> T | None:
        stmt = select(self.model).where(self.model.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_field(self, field: str, value: Any) -> T | None:
        column = getattr(self.model, field, None)
        if column is None:
            return None
        stmt = select(self.model).where(column == value)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def find_all(
        self,
        filters: list[FilterCondition] | None = None,
        sorting: list[SortParam] | None = None,
        pagination: PaginationParams | None = None,
    ) -> PaginatedResult:
        total = await self.count(filters)
        stmt = select(self.model)
        stmt = self._apply_filters(stmt, filters)
        stmt = self._apply_sorting(stmt, sorting)

        if pagination:
            offset = (pagination.page - 1) * pagination.page_size
            stmt = stmt.offset(offset).limit(pagination.page_size)
            total_pages = max(1, (total + pagination.page_size - 1) // pagination.page_size)
            return PaginatedResult(
                items=(await self.db.execute(stmt)).scalars().all(),
                total=total,
                page=pagination.page,
                page_size=pagination.page_size,
                total_pages=total_pages,
                has_next=pagination.page < total_pages,
                has_previous=pagination.page > 1,
            )

        return PaginatedResult(
            items=(await self.db.execute(stmt)).scalars().all(),
            total=total,
            page=1,
            page_size=total,
            total_pages=1,
            has_next=False,
            has_previous=False,
        )

    async def create(self, entity: T) -> T:
        self.db.add(entity)
        await self.db.flush()
        await self.db.refresh(entity)
        return entity

    async def bulk_create(self, entities: list[T]) -> list[T]:
        self.db.add_all(entities)
        await self.db.flush()
        return entities

    async def update(self, entity: T) -> T:
        await self.db.merge(entity)
        await self.db.flush()
        return entity

    async def delete(self, entity: T, soft: bool = True) -> None:
        if soft and hasattr(entity, "is_deleted"):
            entity.is_deleted = True
            entity.deleted_at = func.now()
            await self.db.merge(entity)
        else:
            await self.db.delete(entity)
        await self.db.flush()

    async def bulk_delete(self, ids: list[UUID], soft: bool = True) -> int:
        if soft and hasattr(self.model, "is_deleted"):
            stmt = (
                update(self.model)
                .where(self.model.id.in_(ids))
                .values(is_deleted=True, deleted_at=func.now())
            )
        else:
            stmt = delete(self.model).where(self.model.id.in_(ids))
        result = await self.db.execute(stmt)
        return result.rowcount

    async def restore(self, id: UUID) -> T | None:
        if not hasattr(self.model, "is_deleted"):
            return None
        entity = await self.get_by_id(id)
        if entity:
            entity.is_deleted = False
            entity.deleted_at = None
            await self.db.merge(entity)
        return entity
