from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.auth.dependencies import require_roles, get_current_user
from app.users.enums import UserRole
from app.database.database import get_db

from .schema import (
    InternalUserCreateRequest,
    RejectUserRequest,
    UserSearchRequest,
    ChangeUserRoleRequest,
    UpdateProfileRequest,
    ChangePasswordRequest,
)

from .service import (
    reject_user,
    search_users,
    get_user_by_id,
    create_internal_user,
    approve_user,
    activate_user,
    deactivate_user,
    change_user_role,
    get_my_profile,
    update_my_profile,
    change_password,
)

router = APIRouter()

# ==========================
# Authorization Roles
# ==========================

READ_ROLES = (
    UserRole.SUPER_ADMIN,
    UserRole.ADMIN,
)

MANAGEMENT_ROLES = (UserRole.SUPER_ADMIN,)


@router.get("/profile")
def get_profile(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_my_profile(
        db,
        current_user["user_id"],
    )


@router.put("/profile")
def update_profile(
    request: UpdateProfileRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return update_my_profile(
        db,
        current_user["user_id"],
        request,
    )


@router.patch("/change-password")
def change_my_password(
    request: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return change_password(
        db,
        current_user["user_id"],
        request,
    )


@router.post(
    "/search",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def search(
    request: UserSearchRequest,
    db: Session = Depends(get_db),
):
    return search_users(
        db,
        request,
    )


@router.get(
    "/{user_id}",
    dependencies=[Depends(require_roles(*READ_ROLES))],
)
def fetch_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_user_by_id(
        db,
        user_id,
    )


@router.post("/register/internal")
def register_internal(
    request: InternalUserCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*MANAGEMENT_ROLES)),
):
    return create_internal_user(
        db,
        request,
        current_user["user_id"],
    )


@router.patch("/{user_id}/approve")
def approve(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*MANAGEMENT_ROLES)),
):
    return approve_user(
        db,
        user_id,
        current_user["user_id"],
    )


@router.patch("/{user_id}/reject")
def reject(
    user_id: int,
    request: RejectUserRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*MANAGEMENT_ROLES)),
):
    return reject_user(
        db,
        user_id,
        current_user["user_id"],
        request,
    )


@router.patch("/{user_id}/activate")
def activate(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*MANAGEMENT_ROLES)),
):
    return activate_user(
        db,
        user_id,
        current_user["user_id"],
    )


@router.patch("/{user_id}/deactivate")
def deactivate(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*MANAGEMENT_ROLES)),
):
    return deactivate_user(
        db,
        user_id,
        current_user["user_id"],
    )


@router.patch("/{user_id}/change-role")
def change_role(
    user_id: int,
    request: ChangeUserRoleRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*MANAGEMENT_ROLES)),
):
    return change_user_role(
        db,
        user_id,
        current_user["user_id"],
        request,
    )
