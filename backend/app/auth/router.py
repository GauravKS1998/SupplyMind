from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from .schema import (
    LoginRequest,
    SignupRequest,
)

from .service import (
    login_user,
    signup_user,
)

router = APIRouter()

# ==========================
# Login
# ==========================


@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):

    return login_user(db, request)


# ==========================
# Public Signup
# ==========================


@router.post("/signup")
def signup(
    request: SignupRequest,
    db: Session = Depends(get_db),
):
    return signup_user(db, request)
