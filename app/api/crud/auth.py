import uuid
from typing import Optional
from typing import Any
from sqlmodel import Session, select
from app.core.security import get_password_hash, verify_password
from app.models.db_models.user import User
from app.models.non_db_models.user import UserCreate, UserUpdate
from .users import get_user_by_email


def authenticate(*, session: Session, email: str, password: str) -> Optional[User]:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.password_hash):
        return None
    return db_user
