from sqlalchemy.orm import Session

from app.auth.jwt import hash_password

from math import ceil

from app.common.responses import PaginatedResponse
from app.common.pagination import PaginationMeta

from app.common.entity_utils import get_or_raise

from .model import User
from .repository import find_by_email, save_user, find_users

from app.logging.logger import logger

from app.auth.jwt import (
    hash_password,
    verify_password,
)

from .enums import ApprovalStatus

from .schema import (
    ExternalRegisterRequest,
    InternalUserCreateRequest,
    UserSearchRequest,
    ChangeUserRoleRequest,
    UpdateProfileRequest,
    ChangePasswordRequest,
)

from .mapper import map_user, map_users

from .exceptions import UserNotFoundException, InvalidCredentialsException

from .validators import (
    validate_email_not_exists,
    validate_user_exists,
    validate_internal_role,
    validate_external_role,
    validate_email_available,
    validate_user_is_approved,
    validate_not_self,
    validate_not_last_super_admin,
    validate_role_not_same,
    validate_same_role_category,
    validate_profile_email_available,
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

    validate_profile_email_available(
        db,
        user_id,
        request.email,
    )

    user.username = request.username
    user.email = request.email

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


def register_external_user(
    db: Session,
    request: ExternalRegisterRequest,
):
    validate_email_not_exists(
        db,
        request.email,
    )

    validate_external_role(
        request.role,
    )

    user = User(
        username=request.username,
        email=request.email,
        password=hash_password(
            request.password,
        ),
        role=request.role,
        approval_status=ApprovalStatus.PENDING,
    )

    saved_user = save_user(db, user)

    db.commit()
    db.refresh(saved_user)

    logger.info(f"External User {saved_user.email} registered successfully")

    return map_user(saved_user)


def create_internal_user(
    db: Session,
    request: InternalUserCreateRequest,
):
    validate_email_not_exists(
        db,
        request.email,
    )

    validate_internal_role(
        request.role,
    )

    user = User(
        username=request.username,
        email=request.email,
        password=hash_password(
            request.password,
        ),
        role=request.role,
        approval_status=request.approval_status,
        is_active=request.is_active,
    )

    saved_user = save_user(db, user)

    db.commit()
    db.refresh(saved_user)

    logger.info(f"Internal user '{saved_user.email}' created successfully.")

    return map_user(saved_user)


def approve_user(
    db: Session,
    user_email: str,
):

    user = get_or_raise(
        find_by_email(db, user_email), UserNotFoundException("User not found.")
    )

    user.approval_status = ApprovalStatus.APPROVED

    db.commit()
    db.refresh(user)

    logger.info(f"User '{user.email}' approved successfully.")

    return {"message": "User approved successfully"}


def activate_user(
    db: Session,
    user_id: int,
):
    logger.info(f"Activating user id={user_id}")

    user = validate_user_exists(
        db,
        user_id,
    )

    if user.is_active:
        return {"message": "User is already active."}

    validate_user_is_approved(
        user,
    )

    user.is_active = True

    db.commit()
    db.refresh(user)

    logger.info(f"User '{user.email}' activated successfully.")

    return {"message": "User activated successfully."}


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

    role_check = validate_role_not_same(
        user,
        request.role,
    )

    if role_check:
        return role_check

    validate_same_role_category(
        user.role,
        request.role,
    )

    user.role = request.role

    db.commit()
    db.refresh(user)

    logger.info(f"Role changed successfully for user '{user.email}'.")

    return {"message": "User role updated successfully."}
