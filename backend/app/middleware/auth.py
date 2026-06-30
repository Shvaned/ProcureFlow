import uuid

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import AuthenticationException, AuthorizationException
from app.core.security import decode_token
from app.dependencies.providers import get_db
from app.models.identity.user import Role, User

security = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    if not credentials:
        raise AuthenticationException("Authentication required")

    payload = decode_token(credentials.credentials)
    if not payload or payload.get("type") != "access":
        raise AuthenticationException("Invalid or expired token")

    user_id = uuid.UUID(payload.get("sub"))
    result = await db.execute(
        select(User).where(User.id == user_id).options(
            selectinload(User.roles).selectinload(Role.permissions)
        )
    )
    user = result.scalar_one_or_none()
    if not user or not user.is_active:
        raise AuthenticationException("User not found or inactive")

    request.state.user_id = str(user.id)
    request.state.request_id = getattr(request.state, "request_id", None)
    return user


class RequirePermission:
    def __init__(self, permission: str):
        self.permission = permission

    async def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        user_permissions: set[str] = set()
        for role in current_user.roles:
            for perm in role.permissions:
                user_permissions.add(perm.name)

        if self.permission not in user_permissions:
            raise AuthorizationException(f"Missing required permission: {self.permission}")
        return current_user


class RequireAnyPermission:
    def __init__(self, *permissions: str):
        self.permissions = permissions

    async def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        user_permissions: set[str] = set()
        for role in current_user.roles:
            for perm in role.permissions:
                user_permissions.add(perm.name)

        if not any(p in user_permissions for p in self.permissions):
            raise AuthorizationException("Insufficient permissions")
        return current_user


class RequireAllPermissions:
    def __init__(self, *permissions: str):
        self.permissions = permissions

    async def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        user_permissions: set[str] = set()
        for role in current_user.roles:
            for perm in role.permissions:
                user_permissions.add(perm.name)

        if not all(p in user_permissions for p in self.permissions):
            raise AuthorizationException("Insufficient permissions")
        return current_user
