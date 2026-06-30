import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.core.exceptions import (
    AuthenticationException, AuthorizationException,
    NotFoundException, ConflictException, ValidationException, BusinessRuleException
)
from app.models.identity.user import User, UserSession, Role, Permission
from app.schemas.auth import (
    LoginResponse, UserCreateRequest, UserUpdateRequest, UserResponse,
    RoleCreateRequest, RoleUpdateRequest, RoleResponse, PermissionResponse,
)


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def login(self, email: str, password: str, ip_address: str | None = None,
                    user_agent: str | None = None) -> LoginResponse:
        from sqlalchemy import select
        from sqlalchemy.orm import selectinload

        result = await self.db.execute(
            select(User).where(User.email == email).options(
                selectinload(User.roles).selectinload(Role.permissions)
            )
        )
        user = result.scalar_one_or_none()

        if not user or not verify_password(password, user.hashed_password):
            raise AuthenticationException("Invalid email or password")

        if not user.is_active:
            raise AuthenticationException("Account is inactive")

        if user.is_locked:
            raise AuthenticationException("Account is locked. Contact your administrator.")

        if user.failed_login_attempts >= 5:
            user.is_locked = True
            await self.db.flush()
            raise AuthenticationException("Account locked due to too many failed attempts")

        access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})

        session = UserSession(
            user_id=user.id,
            refresh_token=refresh_token,
            ip_address=ip_address,
            browser=user_agent or "",
        )
        self.db.add(session)

        user.last_login_at = datetime.now(timezone.utc)
        user.last_login_ip = ip_address
        user.failed_login_attempts = 0
        await self.db.flush()

        permissions = []
        for role in user.roles:
            for perm in role.permissions:
                if perm.name not in permissions:
                    permissions.append(perm.name)

        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserResponse(
                id=str(user.id),
                email=user.email,
                name=user.name,
                is_active=user.is_active,
                is_locked=user.is_locked,
                roles=[RoleResponse(
                    id=str(r.id), name=r.name, description=r.description, is_system=r.is_system,
                    permissions=[]
                ) for r in user.roles],
                permissions=permissions,
            ),
        )

    async def logout(self, user_id: uuid.UUID, refresh_token: str | None = None) -> None:
        from sqlalchemy import select, update
        if refresh_token:
            await self.db.execute(
                update(UserSession)
                .where(UserSession.user_id == user_id, UserSession.refresh_token == refresh_token)
                .values(is_revoked=True)
            )
        else:
            await self.db.execute(
                update(UserSession)
                .where(UserSession.user_id == user_id)
                .values(is_revoked=True)
            )
        await self.db.flush()

    async def refresh_token(self, refresh_token: str) -> dict:
        from sqlalchemy import select
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise AuthenticationException("Invalid refresh token")

        result = await self.db.execute(
            select(UserSession).where(
                UserSession.refresh_token == refresh_token,
                UserSession.is_revoked == False,
            )
        )
        session = result.scalar_one_or_none()
        if not session:
            raise AuthenticationException("Session revoked or not found")

        session.is_revoked = True

        user_id = uuid.UUID(payload["sub"])
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise AuthenticationException("User not found")

        new_access = create_access_token(data={"sub": str(user.id), "email": user.email})
        new_refresh = create_refresh_token(data={"sub": str(user.id)})

        new_session = UserSession(user_id=user.id, refresh_token=new_refresh)
        self.db.add(new_session)
        await self.db.flush()

        return {"access_token": new_access, "refresh_token": new_refresh, "token_type": "bearer"}

    async def get_current_user(self, user_id: uuid.UUID) -> UserResponse:
        from sqlalchemy import select
        from sqlalchemy.orm import selectinload

        result = await self.db.execute(
            select(User).where(User.id == user_id).options(
                selectinload(User.roles).selectinload(Role.permissions)
            )
        )
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundException("User not found")

        permissions = []
        for role in user.roles:
            for perm in role.permissions:
                if perm.name not in permissions:
                    permissions.append(perm.name)

        return UserResponse(
            id=str(user.id), email=user.email, name=user.name,
            is_active=user.is_active, is_locked=user.is_locked,
            roles=[RoleResponse(
                id=str(r.id), name=r.name, description=r.description, is_system=r.is_system, permissions=[]
            ) for r in user.roles],
            permissions=permissions,
        )

    async def change_password(self, user_id: uuid.UUID, current_password: str, new_password: str) -> None:
        from sqlalchemy import select
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundException("User not found")
        if not verify_password(current_password, user.hashed_password):
            raise ValidationException("Current password is incorrect")
        user.hashed_password = hash_password(new_password)
        await self.db.flush()


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_users(self) -> list[UserResponse]:
        from sqlalchemy import select
        from sqlalchemy.orm import selectinload
        result = await self.db.execute(
            select(User).options(selectinload(User.roles).selectinload(Role.permissions))
        )
        users = result.scalars().all()
        return [self._to_response(u) for u in users]

    async def get_user(self, user_id: uuid.UUID) -> UserResponse:
        from sqlalchemy import select
        from sqlalchemy.orm import selectinload
        result = await self.db.execute(
            select(User).where(User.id == user_id).options(
                selectinload(User.roles).selectinload(Role.permissions)
            )
        )
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundException("User not found")
        return self._to_response(user)

    async def create_user(self, dto: UserCreateRequest) -> UserResponse:
        from sqlalchemy import select
        result = await self.db.execute(select(User).where(User.email == dto.email))
        if result.scalar_one_or_none():
            raise ConflictException("User with this email already exists")

        user = User(
            email=dto.email,
            name=dto.name,
            hashed_password=hash_password(dto.password),
        )
        if dto.role_ids:
            role_result = await self.db.execute(
                select(Role).where(Role.id.in_([uuid.UUID(r) for r in dto.role_ids]))
            )
            user.roles = list(role_result.scalars().all())

        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return self._to_response(user)

    async def update_user(self, user_id: uuid.UUID, dto: UserUpdateRequest) -> UserResponse:
        from sqlalchemy import select
        from sqlalchemy.orm import selectinload
        result = await self.db.execute(
            select(User).where(User.id == user_id).options(
                selectinload(User.roles).selectinload(Role.permissions)
            )
        )
        user = result.scalar_one_or_none()
        if not user:
            raise NotFoundException("User not found")

        if dto.name is not None:
            user.name = dto.name
        if dto.is_active is not None:
            user.is_active = dto.is_active
        if dto.role_ids is not None:
            role_result = await self.db.execute(
                select(Role).where(Role.id.in_([uuid.UUID(r) for r in dto.role_ids]))
            )
            user.roles = list(role_result.scalars().all())

        await self.db.flush()
        return self._to_response(user)

    def _to_response(self, user: User) -> UserResponse:
        permissions = []
        for role in user.roles:
            for perm in role.permissions:
                if perm.name not in permissions:
                    permissions.append(perm.name)
        return UserResponse(
            id=str(user.id), email=user.email, name=user.name,
            is_active=user.is_active, is_locked=user.is_locked,
            roles=[RoleResponse(
                id=str(r.id), name=r.name, description=r.description, is_system=r.is_system, permissions=[]
            ) for r in user.roles],
            permissions=permissions,
        )
