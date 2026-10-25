from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.security import decode_access_token

bearer_scheme = HTTPBearer(auto_error=False)
DbSession = Annotated[Session, Depends(get_db)]
Credentials = Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)]


def get_current_user(credentials: Credentials, db: DbSession) -> User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required or token is invalid.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise unauthorized
    try:
        payload = decode_access_token(credentials.credentials)
        subject = payload.get("sub")
        if not isinstance(subject, str) or not subject.isdigit():
            raise unauthorized
        user = db.get(User, int(subject))
    except (jwt.InvalidTokenError, RuntimeError, ValueError):
        raise unauthorized
    if user is None or not user.is_active:
        raise unauthorized
    # Do not trust role or ownership claims from a token; load current values from DB.
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_roles(*roles: str):
    def dependency(user: CurrentUser) -> User:
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )
        return user
    return dependency


AdmissionStaff = Annotated[User, Depends(require_roles("admin", "admission_staff"))]
StudentStaff = Annotated[User, Depends(require_roles("admin", "admission_staff"))]
AdminUser = Annotated[User, Depends(require_roles("admin"))]
