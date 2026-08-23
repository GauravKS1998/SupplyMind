from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.common.pagination import PaginationRequest

from .enums import UserRole, ApprovalStatus

# ==========================
# Internal User Creation
# ==========================


class InternalUserCreateRequest(BaseModel):
    full_name: str

    email: EmailStr
    phone: str | None = None

    password: str

    role: UserRole


# ==========================
# User Response
# ==========================


class UserResponse(BaseModel):
    id: int

    full_name: str

    email: EmailStr
    phone: str | None

    role: UserRole
    approval_status: ApprovalStatus

    is_active: bool

    approved_by: int | None
    approved_at: datetime | None

    rejected_by: int | None
    rejected_at: datetime | None
    rejection_reason: str | None

    created_by: int | None
    created_at: datetime

    updated_at: datetime


# ==========================
# Search
# ==========================


class UserSearchRequest(PaginationRequest):
    role: UserRole | None = None

    approval_status: ApprovalStatus | None = None
    is_active: bool | None = None


# ==========================
# Profile
# ==========================


class UpdateProfileRequest(BaseModel):
    full_name: str
    phone: str | None = None


# ==========================
# Password
# ==========================


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


# ==========================
# Role
# ==========================


class ChangeUserRoleRequest(BaseModel):
    role: UserRole


# ==========================
# Approval
# ==========================


class RejectUserRequest(BaseModel):
    reason: str
