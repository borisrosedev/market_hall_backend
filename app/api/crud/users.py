import uuid
from typing import Any
from sqlmodel import Session, select
from app.core.security import get_password_hash, verify_password
from app.models.db_models.user import User
from app.models.non_db_models.user import UserCreate, UserUpdate


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create,
        update={"password_hash": get_password_hash(user_create.password.get_secret_value())},
    )

    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_all_users(*, session: Session) -> list[User] | None:
    statement = select(User).order_by(User.created_at.desc())
    return list(session.exec(statement=statement).all())


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user
