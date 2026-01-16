import enum
from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from ...database import db


class UserRoles(enum.Enum):
    standard = "standard"
    premium = "premium"
    admin = "admin"


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    is_banned: Mapped[bool] = mapped_column(nullable=False, default=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    photo_name: Mapped[Optional[str]] = mapped_column(nullable=True)
    role: Mapped[UserRoles] = mapped_column(Enum(UserRoles), default=UserRoles.standard)

    # one-to-one
    cart: Mapped[Optional["Cart"]] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        single_parent=True,
    )

    # one-to-many
    notifications: Mapped[List["Notification"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
        single_parent=True,
        order_by="desc(Notification.created_at)",
    )

    created_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    @property
    def password(self):
        raise Exception("password is write-only")

    @password.setter
    def password(self, plain_password: str):
        self.password_hash = generate_password_hash(plain_password, method="pbkdf2:sha256:600000")

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def get_fullname(self) -> str:
        return f"{self.firstname.capitalize()} {self.lastname.capitalize()}"

    def to_dict(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "is_banned": self.is_banned,
            "role": self.role.value,
            "photo_name": self.photo_name,
            "fullname": self.get_fullname(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "cart_id": self.cart.id,
        }
