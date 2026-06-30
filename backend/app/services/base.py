from typing import Generic, TypeVar
from uuid import UUID

from app.repositories.base import (
    BaseRepository,
    FilterCondition,
    PaginatedResult,
    PaginationParams,
    SortParam,
)

T = TypeVar("T")


class UnitOfWork:
    def __init__(self, db):
        self.db = db
        self._committed = False

    async def commit(self):
        await self.db.commit()
        self._committed = True

    async def rollback(self):
        await self.db.rollback()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
            return False
        if not self._committed:
            await self.commit()
        return False


class BaseService(Generic[T]):
    repository: BaseRepository[T]

    def __init__(self, repository: BaseRepository[T]):
        self.repository = repository

    async def get_by_id(self, id: UUID) -> T | None:
        return await self.repository.get_by_id(id)

    async def exists(self, id: UUID) -> bool:
        return await self.repository.exists(id)

    async def find_all(
        self,
        filters: list[FilterCondition] | None = None,
        sorting: list[SortParam] | None = None,
        pagination: PaginationParams | None = None,
    ) -> PaginatedResult:
        return await self.repository.find_all(filters, sorting, pagination)

    async def delete(self, id: UUID, soft: bool = True) -> None:
        entity = await self.repository.get_by_id(id)
        if entity:
            await self.repository.delete(entity, soft=soft)


class CRUDService(BaseService[T]):
    async def create(self, entity: T) -> T:
        return await self.repository.create(entity)

    async def update(self, entity: T) -> T:
        return await self.repository.update(entity)

    async def bulk_create(self, entities: list[T]) -> list[T]:
        return await self.repository.bulk_create(entities)

    async def bulk_delete(self, ids: list[UUID], soft: bool = True) -> int:
        return await self.repository.bulk_delete(ids, soft=soft)

    async def restore(self, id: UUID) -> T | None:
        return await self.repository.restore(id)
