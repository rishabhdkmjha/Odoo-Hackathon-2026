"""
Reusable FastAPI dependencies for authentication and role-based access control.
"""
from typing import List

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.security import decode_access_token
from app.database.database import get_db
from app.models.user import User
from app.models.enums import RoleEnum, UserStatusEnum

# tokenUrl is documentation-only here since login is JSON-based, not form-based
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        raise credentials_exception

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    if user.status == UserStatusEnum.INACTIVE:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is inactive")

    return user


def require_roles(*allowed_roles: RoleEnum):
    """
    Dependency factory for role-based access control.
    Usage: current_user: User = Depends(require_roles(RoleEnum.ADMIN))
    """

    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This action requires one of the following roles: "
                f"{[r.value for r in allowed_roles]}",
            )
        return current_user

    return role_checker


# Convenience shorthand dependencies used across routers
require_admin = require_roles(RoleEnum.ADMIN)
require_asset_manager = require_roles(RoleEnum.ADMIN, RoleEnum.ASSET_MANAGER)
require_manager_or_head = require_roles(
    RoleEnum.ADMIN, RoleEnum.ASSET_MANAGER, RoleEnum.DEPARTMENT_HEAD
)
require_any_authenticated = require_roles(
    RoleEnum.ADMIN, RoleEnum.ASSET_MANAGER, RoleEnum.DEPARTMENT_HEAD, RoleEnum.EMPLOYEE
)
