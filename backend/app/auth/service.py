from sqlalchemy.orm import Session

from app.users.repository import find_by_email

from .jwt import verify_password, create_access_token

from .schema import (
    LoginRequest,
    AuthResponse,
)

from app.users.enums import ApprovalStatus

from .exceptions import (
    InvalidCredentialsException,
    AccountPendingApprovalException,
)


def login_user(db: Session, request: LoginRequest):
    user = find_by_email(db, request.email)

    if not user:
        raise InvalidCredentialsException("Invalid credentials")

    if not verify_password(request.password, user.password):
        raise InvalidCredentialsException("Invalid credentials")

    if user.approval_status != ApprovalStatus.APPROVED:
        raise AccountPendingApprovalException("Account pending approval")

    access_token = create_access_token(
        {"sub": user.email, "user_id": user.id, "role": user.role.value}
    )

    return AuthResponse(access_token=access_token, token_type="Bearer")
