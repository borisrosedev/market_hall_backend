from datetime import datetime, timedelta, timezone
from typing import Any, Optional
from uuid import UUID

import jwt, logging
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

ALGORITHM = "HS256"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _extract_user_fields(obj: Any) -> tuple[Optional[str], Optional[str], Optional[str]]:

    # Dict-like
    if isinstance(obj, dict):
        uid = obj.get("user_id") or obj.get("id")
        email = obj.get("email")
        role = obj.get("role")
        return (str(uid) if uid is not None else None, email, role)

    # ORM
    uid = getattr(obj, "id", None)
    email = getattr(obj, "email", None)
    role = getattr(obj, "role", None)
    if uid is not None or email is not None or role is not None:
        return (str(uid) if uid is not None else None, email, getattr(role, "value", role))

    if isinstance(obj, (UUID, int, str)):
        return (str(obj), None, None)

    return (None, None, None)



def create_access_token(subject: Any, expires_delta: timedelta) -> str:
    now = datetime.now(timezone.utc)
    exp = now + expires_delta

    user_id, email, role = _extract_user_fields(subject)
    if user_id is None:
        user_id = str(subject)

    claims = {
        "sub": user_id,                         
        "iat": int(now.timestamp()),
        "nbf": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }

    if any([user_id, email, role]):
        claims["usr"] = {
            "user_id": user_id,
            "email": email,
            "role": getattr(role, "value", role),
        }

    return jwt.encode(claims, settings.SECRET_KEY, algorithm=ALGORITHM)




def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)