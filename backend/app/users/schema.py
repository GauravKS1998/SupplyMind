from pydantic import BaseModel, EmailStr

from datetime import datetime

from app.common.pagination import PaginationRequest, PaginationMeta
from app.common.responses import PaginatedResponse

from .enums import UserRole, ApprovalStatus


class ExternalRegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole


class InternalUserCreateRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole
    approval_status: ApprovalStatus
    is_active: bool = True


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole
    approval_status: ApprovalStatus
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserSearchRequest(PaginationRequest):
    role: UserRole | None = None
    approval_status: ApprovalStatus | None = None
    is_active: bool | None = None


class ChangeUserRoleRequest(BaseModel):
    role: UserRole


class UpdateProfileRequest(BaseModel):
    username: str
    email: EmailStr


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
