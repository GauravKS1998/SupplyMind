from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database.database import get_db

from .schema import LoginRequest

from .service import (
    login_user,
)

from .exceptions import (
    InvalidCredentialsException,
    AccountPendingApprovalException,
)

router = APIRouter()


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    try:
        return login_user(db, request)
    except InvalidCredentialsException as e:
        raise HTTPException(status_code=401, detail=str(e))
    except AccountPendingApprovalException as e:
        raise HTTPException(status_code=403, detail=str(e))
