from .model import User
from .schema import UserResponse


def map_user(
    user: User,
) -> UserResponse:

    return UserResponse(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        phone=user.phone,
        role=user.role,
        approval_status=user.approval_status,
        is_active=user.is_active,
        approved_by=user.approved_by,
        approved_at=user.approved_at,
        rejected_by=user.rejected_by,
        rejected_at=user.rejected_at,
        rejection_reason=user.rejection_reason,
        created_by=user.created_by,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


def map_users(
    users: list[User],
):

    return [map_user(user) for user in users]
