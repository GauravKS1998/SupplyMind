from sqlalchemy.orm import Session

from .model import User
from .repository import find_by_email, save_user

from .security import hash_password, verify_password, create_access_token

from .schema import (
    ExternalRegisterRequest,
    InternalUserCreateRequest,
    LoginRequest,
    AuthResponse,
    UserResponse,
)

from .constants import INTERNAL_ROLES, EXTERNAL_ROLES
from .enums import ApprovalStatus

from .exceptions import (
    UserAlreadyExistsException,
    InvalidCredentialsException,
    UserNotFoundException,
    AccountPendingApprovalException,
    InvalidRoleException,
)


def register_external_user(db: Session, request: ExternalRegisterRequest):
    existing_user = find_by_email(db, request.email)

    if existing_user:
        raise UserAlreadyExistsException("Email already exists")

    if request.role not in EXTERNAL_ROLES:
        raise InvalidRoleException("Invalid external role")

    user = User(
        username=request.username,
        email=request.email,
        password=hash_password(request.password),
        role=request.role,
        approval_status=ApprovalStatus.PENDING,
    )

    saved_user = save_user(db, user)

    return UserResponse(
        id=saved_user.id,
        username=saved_user.username,
        email=saved_user.email,
        role=saved_user.role,
        approval_status=saved_user.approval_status,
    )


def create_internal_user(db: Session, request: InternalUserCreateRequest):
    existing_user = find_by_email(db, request.email)

    if existing_user:
        raise UserAlreadyExistsException("Email already exists")

    if request.role not in INTERNAL_ROLES:
        raise InvalidRoleException("Invalid internal role")

    user = User(
        username=request.username,
        email=request.email,
        password=hash_password(request.password),
        role=request.role,
        approval_status=request.approval_status,
        is_active=request.is_active,
    )

    saved_user = save_user(db, user)

    return UserResponse(
        id=saved_user.id,
        username=saved_user.username,
        email=saved_user.email,
        role=saved_user.role,
        approval_status=saved_user.approval_status,
    )


def login_user(db: Session, request: LoginRequest):
    user = find_by_email(db, request.email)

    if not user:
        raise InvalidCredentialsException("Invalid credentials")

    if not verify_password(request.password, user.password):
        raise InvalidCredentialsException("Invalid credentials")

    if user.approval_status != ApprovalStatus.APPROVED:
        raise AccountPendingApprovalException("Account pending approval")

    access_token = create_access_token({"sub": user.email, "role": user.role})

    return AuthResponse(access_token=access_token, token_type="Bearer")


def approve_user(db: Session, user_email: str):
    user = find_by_email(db, user_email)
    if not user:
        raise UserNotFoundException("User not found")

    user.approval_status = "APPROVED"
    db.commit()
    db.refresh(user)

    return {"message": "User approved successfully"}
