from sqlalchemy.orm import Session

from app.common.entity_utils import get_or_raise

from .repository import find_by_id, find_by_email, count_active_super_admins

from .model import User

from .constants import (
    INTERNAL_ROLES,
    EXTERNAL_ROLES,
)

from .enums import UserRole, ApprovalStatus

from .exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
    InvalidRoleException,
    InvalidUserStateException,
)


def validate_email_not_exists(
    db: Session,
    email: str,
):
    existing_user = find_by_email(
        db,
        email,
    )

    if existing_user:
        raise UserAlreadyExistsException("Email already exists.")


def validate_user_exists(
    db: Session,
    user_id: int,
):
    user = get_or_raise(
        find_by_id(db, user_id), UserNotFoundException("User not found.")
    )

    return user


def validate_internal_role(
    role,
):
    if role not in INTERNAL_ROLES:
        raise InvalidRoleException("Invalid internal role.")


def validate_external_role(
    role,
):
    if role not in EXTERNAL_ROLES:
        raise InvalidRoleException("Invalid external role.")


def validate_email_available(
    db: Session,
    user_id: int,
    email: str,
):
    existing_user = find_by_email(
        db,
        email,
    )

    if existing_user and existing_user.id != user_id:
        raise UserAlreadyExistsException("Email already exists.")


def validate_user_is_approved(
    user: User,
):
    if user.approval_status != ApprovalStatus.APPROVED:
        raise InvalidUserStateException("Only approved users can be activated.")


def validate_not_last_super_admin(
    db: Session,
    user: User,
):
    if user.role != UserRole.SUPER_ADMIN:
        return

    total_super_admins = count_active_super_admins(db)

    if total_super_admins <= 1:
        raise InvalidUserStateException("Cannot deactivate the last SUPER_ADMIN.")


def validate_not_self(
    current_user_id: int,
    target_user_id: int,
):
    if current_user_id == target_user_id:
        raise InvalidUserStateException("You cannot deactivate your own account.")


def validate_role_not_same(
    user: User,
    new_role: UserRole,
):
    if user.role == new_role:
        return {"message": "User already has this role."}

    return None


def validate_same_role_category(
    current_role: UserRole,
    new_role: UserRole,
):
    current_internal = current_role in INTERNAL_ROLES
    new_internal = new_role in INTERNAL_ROLES

    if current_internal != new_internal:
        raise InvalidRoleException("Cannot change between internal and external roles.")


def validate_profile_email_available(
    db: Session,
    user_id: int,
    email: str,
):
    existing_user = find_by_email(
        db,
        email,
    )

    if existing_user and existing_user.id != user_id:
        raise UserAlreadyExistsException("Email already exists.")
