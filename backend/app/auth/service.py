from sqlalchemy.orm import Session

from app.users.enums import ApprovalStatus, UserRole
from app.users.model import User
from app.users.repository import find_by_email

from app.suppliers.model import Supplier

from .exceptions import (
    AccountInactiveException,
    AccountNotApprovedException,
    AccountPendingApprovalException,
    InvalidCredentialsException,
    InvalidSignupRoleException,
)

from app.users.exceptions import UserAlreadyExistsException

from .jwt import (
    create_access_token,
    hash_password,
    verify_password,
)

from .schema import (
    AuthResponse,
    AuthUserResponse,
    LoginRequest,
    SignupRequest,
    SignupResponse,
)

PUBLIC_SIGNUP_ROLES = {
    UserRole.SUPPLIER,
    UserRole.CUSTOMER,
}


def login_user(
    db: Session,
    request: LoginRequest,
) -> AuthResponse:

    user = find_by_email(
        db,
        request.email,
    )

    if not user:
        raise InvalidCredentialsException("Invalid credentials.")

    if not verify_password(
        request.password,
        user.password_hash,
    ):
        raise InvalidCredentialsException("Invalid credentials")

    if user.approval_status == ApprovalStatus.PENDING:
        raise AccountPendingApprovalException("Your account is pending approval.")

    if user.approval_status == ApprovalStatus.REJECTED:
        raise AccountNotApprovedException("Your account registration was rejected.")

    if not user.is_active:
        raise AccountInactiveException("Your account is currently inactive.")

    access_token = create_access_token(
        {"sub": user.email, "user_id": user.id, "role": user.role.value}
    )

    return AuthResponse(
        access_token=access_token,
        token_type="Bearer",
        user=AuthUserResponse(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            role=user.role,
        ),
    )


def signup_user(
    db: Session,
    request: SignupRequest,
) -> SignupResponse:

    if request.account_type not in PUBLIC_SIGNUP_ROLES:
        raise InvalidSignupRoleException(
            "Only Supplier and Customer accounts can be created through public signup."
        )

    existing_user = find_by_email(
        db,
        request.email,
    )

    if existing_user:
        raise UserAlreadyExistsException("An account with this email already exists.")

    user = User(
        full_name=request.full_name,
        email=request.email,
        phone=request.phone,
        password_hash=hash_password(
            request.password,
        ),
        role=request.account_type,
        # Public users must wait for approval.
        approval_status=ApprovalStatus.PENDING,
        # Cannot login until approved.
        is_active=False,
    )

    db.add(user)

    try:
        db.flush()

        if request.account_type == UserRole.SUPPLIER:
            supplier = Supplier(
                user_id=user.id,
                company_name=request.company_name,
                contact_person=request.full_name,
                phone=request.phone,
                email=request.email,
            )

            db.add(supplier)

        elif request.account_type == UserRole.CUSTOMER:
            pass

        db.commit()
        db.refresh(user)

    except Exception:
        db.rollback()
        raise

    return SignupResponse(
        message=(
            "Account created successfully. "
            "Your account is pending approval. "
            "You will be able to log in once your account is approved."
        )
    )
