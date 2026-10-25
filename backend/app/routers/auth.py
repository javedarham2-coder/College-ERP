from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.auth import CurrentUser, DbSession
from app.config import settings
from app.models.user import User
from app.schemas.auth import CurrentUserRead, LoginRequest, TokenResponse
from app.security import create_access_token, verify_password

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: DbSession):
    try:
        user = db.scalar(select(User).where(func.lower(User.email) == payload.email.lower()))
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=503, detail="Authentication service unavailable.") from exc

    # Use a generic response for unknown users and incorrect passwords.
    if user is None or not user.is_active or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        token = create_access_token(user_id=user.id, role=user.role, student_id=user.student_id)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail="Authentication is not configured.") from exc
    return TokenResponse(
        access_token=token,
        expires_in=settings.jwt_access_token_expire_minutes * 60,
    )


@router.get("/me", response_model=CurrentUserRead)
def get_me(user: CurrentUser):
    return user
