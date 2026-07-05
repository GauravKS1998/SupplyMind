from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database.database import get_db

from .schema import ExternalRegisterRequest, InternalUserCreateRequest, LoginRequest

from .service import (
    register_external_user,
    create_internal_user,
    login_user,
    approve_user,
)

from .exceptions import (
    UserAlreadyExistsException,
    InvalidCredentialsException,
    UserNotFoundException,
    AccountPendingApprovalException,
)

router = APIRouter()


@router.post("/register")
def register(request: ExternalRegisterRequest, db: Session = Depends(get_db)):
    try:
        return register_external_user(db, request)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/internal/create")
def create_internal(request: InternalUserCreateRequest, db: Session = Depends(get_db)):
    try:
        return create_internal_user(db, request)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    try:
        return login_user(db, request)
    except InvalidCredentialsException as e:
        raise HTTPException(status_code=401, detail=str(e))
    except AccountPendingApprovalException as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.put("/approve/{email}")
def approve(email: str, db: Session = Depends(get_db)):
    try:
        return approve_user(db, email)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
