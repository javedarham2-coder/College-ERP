"""Password hashing and JWT helpers for the College ERP API."""

import base64
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from app.config import settings

_PASSWORD_SCHEME = "scrypt"
_SCRYPT_N = 2**14
_SCRYPT_R = 8
_SCRYPT_P = 1
_SALT_BYTES = 16
_KEY_BYTES = 32


def hash_password(password: str) -> str:
    """Hash a password with scrypt and a fresh cryptographically random salt."""
    if len(password) < 12:
        raise ValueError("Passwords must be at least 12 characters long.")
    salt = secrets.token_bytes(_SALT_BYTES)
    digest = hashlib.scrypt(
        password.encode("utf-8"), salt=salt, n=_SCRYPT_N,
        r=_SCRYPT_R, p=_SCRYPT_P, dklen=_KEY_BYTES,
    )
    encode = lambda value: base64.urlsafe_b64encode(value).decode("ascii")
    return f"{_PASSWORD_SCHEME}${_SCRYPT_N}${_SCRYPT_R}${_SCRYPT_P}${encode(salt)}${encode(digest)}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        scheme, n, r, p, salt_text, digest_text = stored_hash.split("$", 5)
        if scheme != _PASSWORD_SCHEME:
            return False
        decode = lambda value: base64.urlsafe_b64decode(value.encode("ascii"))
        salt, expected = decode(salt_text), decode(digest_text)
        actual = hashlib.scrypt(
            password.encode("utf-8"), salt=salt, n=int(n), r=int(r),
            p=int(p), dklen=len(expected),
        )
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError, UnicodeError):
        return False


def create_access_token(*, user_id: int, role: str, student_id: int | None = None) -> str:
    if not settings.jwt_secret_key or len(settings.jwt_secret_key) < 32:
        raise RuntimeError("JWT_SECRET_KEY must be configured with at least 32 characters.")
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": str(user_id),
        "role": role,
        "iat": now,
        "exp": now + timedelta(minutes=settings.jwt_access_token_expire_minutes),
    }
    if student_id is not None:
        payload["student_id"] = student_id
    return jwt.encode(payload, settings.jwt_secret_key, algorithm="HS256")


def decode_access_token(token: str) -> dict[str, Any]:
    if not settings.jwt_secret_key or len(settings.jwt_secret_key) < 32:
        raise RuntimeError("JWT_SECRET_KEY must be configured with at least 32 characters.")
    return jwt.decode(token, settings.jwt_secret_key, algorithms=["HS256"])
