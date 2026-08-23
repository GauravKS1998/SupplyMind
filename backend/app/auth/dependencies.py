from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from .jwt import (
    SECRET_KEY,
    ALGORITHM,
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = payload.get("user_id")
        email = payload.get("sub")
        role = payload.get("role")

        if not user_id or not email or not role:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_roles(*allowed_roles):
    def role_checker(
        current_user=Depends(get_current_user),
    ):
        if current_user["role"] not in [role.value for role in allowed_roles]:
            raise HTTPException(
                status_code=403,
                detail="Access denied",
            )

        return current_user

    return role_checker
