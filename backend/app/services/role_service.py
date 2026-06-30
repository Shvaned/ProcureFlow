import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.identity.user import Role, Permission
from app.core.exceptions import NotFoundException, ConflictException
from app.schemas.auth import RoleCreateRequest, RoleUpdateRequest


class RoleService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_roles(self) -> list[Role]:
        result = await self.db.execute(
            select(Role).options(selectinload(Role.permissions))
        )
        return list(result.scalars().all())

    async def get_role(self, role_id: uuid.UUID) -> Role:
        result = await self.db.execute(
            select(Role).where(Role.id == role_id).options(selectinload(Role.permissions))
        )
        role = result.scalar_one_or_none()
        if not role:
            raise NotFoundException("Role not found")
        return role

    async def create_role(self, dto: RoleCreateRequest) -> Role:
        result = await self.db.execute(select(Role).where(Role.name == dto.name))
        if result.scalar_one_or_none():
            raise ConflictException(f"Role '{dto.name}' already exists")

        role = Role(name=dto.name, description=dto.description)
        if dto.permission_ids:
            perm_result = await self.db.execute(
                select(Permission).where(
                    Permission.id.in_([uuid.UUID(p) for p in dto.permission_ids])
                )
            )
            role.permissions = list(perm_result.scalars().all())

        self.db.add(role)
        await self.db.flush()
        return role

    async def update_role(self, role_id: uuid.UUID, dto: RoleUpdateRequest) -> Role:
        role = await self.get_role(role_id)
        if dto.name is not None:
            role.name = dto.name
        if dto.description is not None:
            role.description = dto.description
        if dto.permission_ids is not None:
            perm_result = await self.db.execute(
                select(Permission).where(
                    Permission.id.in_([uuid.UUID(p) for p in dto.permission_ids])
                )
            )
            role.permissions = list(perm_result.scalars().all())
        await self.db.flush()
        return role


class PermissionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_permissions(self) -> list[Permission]:
        result = await self.db.execute(select(Permission))
        return list(result.scalars().all())

    async def list_permission_groups(self) -> list[str]:
        result = await self.db.execute(select(Permission.group).distinct())
        return [row[0] for row in result.all()]
