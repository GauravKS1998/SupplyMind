from datetime import datetime, timezone

from sqlalchemy.orm import Session

from math import ceil

from app.common.responses import PaginatedResponse
from app.common.pagination import PaginationMeta

from .model import User
from .repository import save_user, find_users

from app.logging.logger import logger

from app.auth.jwt import (
    hash_password,
    verify_password,
)

from .enums import ApprovalStatus, UserRole

from .schema import (
    InternalUserCreateRequest,
    RejectUserRequest,
    UserSearchRequest,
    ChangeUserRoleRequest,
    UpdateProfileRequest,
    ChangePasswordRequest,
)

from .mapper import map_user, map_users

from .exceptions import InvalidUserStateException
from app.auth.exceptions import InvalidCredentialsException

from .validators import (
    validate_email_not_exists,
    validate_user_exists,
    validate_internal_role,
    validate_user_is_approved,
    validate_not_self,
    validate_not_last_super_admin,
    validate_role_not_same,
    validate_same_role_category,
)

# ==========================
# Self-service
# ==========================


def get_my_profile(
    db: Session,
    user_id: int,
):
    logger.info(f"Fetching profile for user id={user_id}")

    user = validate_user_exists(
        db,
        user_id,
    )

    return map_user(
        user,
    )


def update_my_profile(
    db: Session,
    user_id: int,
    request: UpdateProfileRequest,
):
    logger.info(f"Updating profile for user id={user_id}")

    user = validate_user_exists(
        db,
        user_id,
    )

    user.full_name = request.full_name
    user.phone = request.phone

    db.commit()
    db.refresh(user)

    logger.info(f"Profile updated successfully for '{user.email}'.")

    return map_user(
        user,
    )


def change_password(
    db: Session,
    user_id: int,
    request: ChangePasswordRequest,
):
    logger.info(f"Changing password for user id={user_id}")

    user = validate_user_exists(
        db,
        user_id,
    )

    if not verify_password(
        request.current_password,
        user.password_hash,
    ):
        raise InvalidCredentialsException("Current password is incorrect.")

    user.password_hash = hash_password(
        request.new_password,
    )

    db.commit()

    logger.info(f"Password changed successfully for '{user.email}'.")

    return {"message": "Password updated successfully."}


# ==========================
# Admin views
# ==========================


def get_user_by_id(
    db: Session,
    user_id: int,
):
    logger.info(f"Fetching user with id={user_id}")

    user = validate_user_exists(
        db,
        user_id,
    )

    return map_user(
        user,
    )


def search_users(
    db: Session,
    request: UserSearchRequest,
):
    logger.info("Searching users.")

    users, total_items = find_users(
        db=db,
        page=request.page,
        size=request.size,
        search=request.search,
        role=request.role,
        approval_status=request.approval_status,
        is_active=request.is_active,
        sort_by=request.sort_by,
        direction=request.direction,
    )

    total_pages = ceil(total_items / request.size) if total_items > 0 else 0

    return PaginatedResponse(
        items=map_users(users),
        pagination=PaginationMeta(
            page=request.page,
            size=request.size,
            total_items=total_items,
            total_pages=total_pages,
            has_next=request.page < total_pages,
            has_previous=request.page > 1,
        ),
    )


# ==========================
# Internal User Creation
# ==========================


def create_internal_user(
    db: Session,
    request: InternalUserCreateRequest,
    current_user_id: int,
):
    validate_email_not_exists(
        db,
        request.email,
    )

    validate_internal_role(
        request.role,
    )

    user = User(
        full_name=request.full_name,
        email=request.email,
        phone=request.phone,
        password_hash=hash_password(request.password),
        role=request.role,
        approval_status=ApprovalStatus.APPROVED,
        is_active=True,
        created_by=current_user_id,
    )

    saved_user = save_user(db, user)

    db.commit()
    db.refresh(saved_user)

    logger.info(
        f"Internal user '{saved_user.email}' " f"created by user id={current_user_id}."
    )

    return map_user(saved_user)


# ==========================
# Approve
# ==========================


def approve_user(
    db: Session,
    user_id: int,
    current_user_id: int,
):

    user = validate_user_exists(
        db,
        user_id,
    )

    if user.approval_status == ApprovalStatus.APPROVED:
        return {"message": "User is already approved."}

    user.approval_status = ApprovalStatus.APPROVED

    user.is_active = True

    user.approved_by = current_user_id
    user.approved_at = datetime.now(timezone.utc)

    user.rejected_by = None
    user.rejected_at = None
    user.rejection_reason = None

    db.commit()
    db.refresh(user)

    logger.info(f"User '{user.email}' approved by " f"user id={current_user_id}.")

    return {"message": "User approved successfully"}


# ==========================
# Reject
# ==========================


def reject_user(
    db: Session,
    user_id: int,
    current_user_id: int,
    request: RejectUserRequest,
):

    user = validate_user_exists(
        db,
        user_id,
    )

    if user.approval_status != ApprovalStatus.PENDING:
        raise InvalidUserStateException("Only pending users can be rejected.")

    user.approval_status = ApprovalStatus.REJECTED
    user.is_active = False

    user.rejected_by = current_user_id
    user.rejected_at = datetime.now(timezone.utc)
    user.rejection_reason = request.reason

    db.commit()
    db.refresh(user)

    logger.info(f"User '{user.email}' rejected by " f"user id={current_user_id}.")

    return {"message": "User rejected successfully."}


# ==========================
# Activate
# ==========================


def activate_user(
    db: Session,
    user_id: int,
    current_user_id: int,
):
    logger.info(f"Activating user id={user_id}")

    user = validate_user_exists(
        db,
        user_id,
    )

    validate_user_is_approved(
        user,
    )

    if user.is_active:
        return {"message": "User is already active."}

    user.is_active = True
    user.reactivated_by = current_user_id
    user.reactivated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(user)

    logger.info(f"User '{user.email}' activated successfully.")

    return {"message": "User activated successfully."}


# ==========================
# Deactivate
# ==========================


def deactivate_user(
    db: Session,
    user_id: int,
    current_user_id: int,
):
    logger.info(f"Deactivating user id={user_id}")

    user = validate_user_exists(
        db,
        user_id,
    )

    if not user.is_active:
        return {"message": "User is already inactive."}

    validate_not_self(
        current_user_id,
        user_id,
    )

    validate_not_last_super_admin(
        db,
        user,
    )

    user.is_active = False
    user.deactivated_by = current_user_id
    user.deactivated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(user)

    logger.info(f"User '{user.email}' deactivated successfully.")

    return {"message": "User deactivated successfully."}


def change_user_role(
    db: Session,
    user_id: int,
    current_user_id: int,
    request: ChangeUserRoleRequest,
):
    logger.info(f"Changing role for user id={user_id}")

    user = validate_user_exists(
        db,
        user_id,
    )

    validate_not_self(
        current_user_id,
        user_id,
    )

    validate_not_last_super_admin(
        db,
        user,
    )

    validate_internal_role(user.role)
    validate_internal_role(request.role)

    validate_same_role_category(
        user.role,
        request.role,
    )

    role_check = validate_role_not_same(
        user,
        request.role,
    )

    if role_check:
        return role_check

    user.role = request.role

    db.commit()
    db.refresh(user)

    logger.info(f"Role changed successfully for user '{user.email}'.")

    return {"message": "User role updated successfully."}
