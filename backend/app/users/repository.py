from sqlalchemy.orm import Session

from sqlalchemy import asc, desc

from sqlalchemy import func

from app.common.filtering import apply_filter
from app.common.search import apply_search
from app.common.sorting import apply_sorting

from .enums import UserRole, ApprovalStatus

from .model import User


def save_user(
    db: Session,
    user: User,
):
    db.add(user)
    db.flush()

    return user


def find_by_email(
    db: Session,
    email: str,
):
    return db.query(User).filter(User.email == email).first()


def find_by_id(
    db: Session,
    user_id: int,
):
    return db.query(User).filter(User.id == user_id).first()


def count_active_super_admins(
    db: Session,
):
    return (
        db.query(User)
        .filter(
            User.role == UserRole.SUPER_ADMIN,
            User.is_active.is_(True),
        )
        .count()
    )


ALLOWED_SORT_FIELDS = {
    "username",
    "email",
    "role",
    "approval_status",
    "created_at",
    "updated_at",
}


def find_users(
    db: Session,
    page: int = 1,
    size: int = 20,
    search: str | None = None,
    role: UserRole | None = None,
    approval_status: ApprovalStatus | None = None,
    is_active: bool | None = None,
    sort_by: str | None = None,
    direction: str = "asc",
):
    query = db.query(User)

    # -----------------------
    # Filtering
    # -----------------------

    query = apply_filter(
        query,
        User,
        role=role,
        approval_status=approval_status,
        is_active=is_active,
    )

    # -----------------------
    # Search
    # -----------------------

    query = apply_search(
        query,
        [
            User.username,
            User.email,
        ],
        search,
    )

    # -----------------------
    # Count
    # -----------------------

    total_items = query.with_entities(func.count(User.id)).scalar()

    # -----------------------
    # Sorting
    # -----------------------

    if sort_by:
        if sort_by not in ALLOWED_SORT_FIELDS:
            sort_by = "created_at"
    else:
        sort_by = "created_at"

    query = apply_sorting(
        query,
        User,
        sort_by,
        direction,
    )

    # -----------------------
    # Pagination
    # -----------------------

    users = query.offset((page - 1) * size).limit(size).all()

    return users, total_items
