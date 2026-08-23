from pydantic import BaseModel, EmailStr, Field

from app.users.enums import UserRole

# ==========================
# Login
# ==========================


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ==========================
# Authenticated User
# ==========================


class AuthUserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: UserRole


# ==========================
# Login Response
# ==========================


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user: AuthUserResponse


# ==========================
# Public Signup
# ==========================


class SignupRequest(BaseModel):
    full_name: str
    email: EmailStr
    phone: str | None = None

    company_name: str

    account_type: UserRole

    password: str


# ==========================
# Signup Response
# ==========================


class SignupResponse(BaseModel):
    message: str
