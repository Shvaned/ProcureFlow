import uuid
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.providers import get_db
from app.services.auth_service import AuthService, UserService
from app.middleware.auth import get_current_user, RequirePermission
from app.schemas.auth import (
    LoginRequest, RefreshRequest, ChangePasswordRequest,
    UserCreateRequest, UserUpdateRequest,
    RoleCreateRequest, RoleUpdateRequest,
)
from app.schemas.common import StandardResponse
from app.models.identity.user import User
from app.services.role_service import RoleService, PermissionService

router = APIRouter()


@router.post("/auth/login")
async def login(request: Request, body: LoginRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    result = await service.login(
        body.email, body.password,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    return StandardResponse.ok(data=result.model_dump(), message="Login successful")


@router.post("/auth/logout")
async def logout(
    request: Request,
    body: dict | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    refresh = body.get("refresh_token") if body else None
    await service.logout(current_user.id, refresh)
    return StandardResponse.ok(message="Logged out successfully")


@router.post("/auth/refresh")
async def refresh(body: RefreshRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    result = await service.refresh_token(body.refresh_token)
    return StandardResponse.ok(data=result, message="Token refreshed")


@router.get("/auth/me")
async def get_me(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    result = await service.get_current_user(current_user.id)
    return StandardResponse.ok(data=result.model_dump())


@router.post("/auth/change-password")
async def change_password(
    body: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    await service.change_password(current_user.id, body.current_password, body.new_password)
    return StandardResponse.ok(message="Password changed successfully")


# User Management
@router.get("/users")
async def list_users(
    _: User = Depends(RequirePermission("Users.Read")),
    db: AsyncSession = Depends(get_db),
):
    service = UserService(db)
    users = await service.list_users()
    return StandardResponse.ok(data=[u.model_dump() for u in users])


@router.get("/users/{user_id}")
async def get_user(
    user_id: uuid.UUID,
    _: User = Depends(RequirePermission("Users.Read")),
    db: AsyncSession = Depends(get_db),
):
    service = UserService(db)
    user = await service.get_user(user_id)
    return StandardResponse.ok(data=user.model_dump())


@router.post("/users")
async def create_user(
    body: UserCreateRequest,
    _: User = Depends(RequirePermission("Users.Write")),
    db: AsyncSession = Depends(get_db),
):
    service = UserService(db)
    user = await service.create_user(body)
    return StandardResponse.ok(data=user.model_dump(), message="User created")


@router.put("/users/{user_id}")
async def update_user(
    user_id: uuid.UUID,
    body: UserUpdateRequest,
    _: User = Depends(RequirePermission("Users.Write")),
    db: AsyncSession = Depends(get_db),
):
    service = UserService(db)
    user = await service.update_user(user_id, body)
    return StandardResponse.ok(data=user.model_dump(), message="User updated")


# Roles
@router.get("/roles")
async def list_roles(
    _: User = Depends(RequirePermission("Users.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = RoleService(db)
    roles = await svc.list_roles()
    return StandardResponse.ok(data=[
        {"id": str(r.id), "name": r.name, "description": r.description,
         "is_system": r.is_system,
         "permissions": [{"id": str(p.id), "name": p.name, "group": p.group} for p in r.permissions]}
        for r in roles
    ])


@router.post("/roles")
async def create_role(
    body: RoleCreateRequest,
    _: User = Depends(RequirePermission("Users.Write")),
    db: AsyncSession = Depends(get_db),
):
    svc = RoleService(db)
    role = await svc.create_role(body)
    return StandardResponse.ok(data={"id": str(role.id), "name": role.name}, message="Role created")


@router.put("/roles/{role_id}")
async def update_role(
    role_id: uuid.UUID,
    body: RoleUpdateRequest,
    _: User = Depends(RequirePermission("Users.Write")),
    db: AsyncSession = Depends(get_db),
):
    svc = RoleService(db)
    role = await svc.update_role(role_id, body)
    return StandardResponse.ok(data={"id": str(role.id), "name": role.name}, message="Role updated")


# Permissions
@router.get("/permissions")
async def list_permissions(
    _: User = Depends(RequirePermission("Users.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = PermissionService(db)
    permissions = await svc.list_permissions()
    return StandardResponse.ok(data=[
        {"id": str(p.id), "name": p.name, "description": p.description, "group": p.group}
        for p in permissions
    ])


@router.get("/permissions/groups")
async def list_permission_groups(
    _: User = Depends(RequirePermission("Users.Read")),
    db: AsyncSession = Depends(get_db),
):
    svc = PermissionService(db)
    groups = await svc.list_permission_groups()
    return StandardResponse.ok(data=groups)
