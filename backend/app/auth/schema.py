from pydantic import BaseModel, EmailStr

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


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole
    approval_status: ApprovalStatus
