from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class LoginRequest(BaseModel):
    email: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=1)


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: "UserResponse"


class RefreshRequest(BaseModel):
    refresh_token: str


class RefreshResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)


class UserCreateRequest(BaseModel):
    email: str = Field(..., min_length=1, max_length=255)
    name: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=8)
    role_ids: list[str] = Field(default_factory=list)


class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None
    role_ids: Optional[list[str]] = None


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    is_active: bool
    is_locked: bool
    roles: list["RoleResponse"] = Field(default_factory=list)
    permissions: list[str] = Field(default_factory=list)


class RoleCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    permission_ids: list[str] = Field(default_factory=list)


class RoleUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    permission_ids: Optional[list[str]] = None


class RoleResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    is_system: bool
    permissions: list["PermissionResponse"] = Field(default_factory=list)


class PermissionResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    group: str
