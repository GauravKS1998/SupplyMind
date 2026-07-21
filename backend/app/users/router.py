from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.auth.dependencies import require_roles, get_current_user
from app.users.enums import UserRole
from app.database.database import get_db

from app.common.responses import PaginatedResponse

from .schema import (
    ExternalRegisterRequest,
    InternalUserCreateRequest,
    UserSearchRequest,
    ChangeUserRoleRequest,
    UpdateProfileRequest,
    ChangePasswordRequest,
)

from .service import (
    search_users,
    get_user_by_id,
    register_external_user,
    create_internal_user,
    approve_user,
    activate_user,
    deactivate_user,
    change_user_role,
    get_my_profile,
    update_my_profile,
    change_password,
)

from .exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
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


@router.post("/register")
def register(request: ExternalRegisterRequest, db: Session = Depends(get_db)):
    try:
        return register_external_user(db, request)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/register/internal")
def register_internal(
    request: InternalUserCreateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*MANAGEMENT_ROLES)),
):
    try:
        return create_internal_user(db, request)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/approve/{email}")
def approve(
    email: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*MANAGEMENT_ROLES)),
):
    try:
        return approve_user(db, email)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch(
    "/{user_id}/activate",
)
def activate(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*MANAGEMENT_ROLES)),
):
    return activate_user(
        db,
        user_id,
    )


@router.patch(
    "/{user_id}/deactivate",
)
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


@router.patch(
    "/{user_id}/change-role",
)
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
