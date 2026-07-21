from .model import User
from .schema import UserResponse


def map_user(
    user: User,
):
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        approval_status=user.approval_status,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


def map_users(
    users: list[User],
):
    return [map_user(user) for user in users]
