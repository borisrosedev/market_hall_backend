import enum
from typing import List, Optional
from sqlalchemy import Integer, String, Enum,CheckConstraint, func, DATETIME  
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db



class UserRoles(enum.Enum):
    """An Enumeration Class interesting in the different user roles"""
    user="user"
    premimum="premium"
    admin="admin"

class User(db.Model):
    __tablename__="users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    firstname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    is_banned: Mapped[bool] = mapped_column(nullable=False, default=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    photo_name: Mapped[str] = mapped_column(nullable=True)
    role: Mapped[UserRoles] = mapped_column(Enum(UserRoles), default=UserRoles.user)
    cart: Mapped[Optional["Cart"]] = relationship(
        back_populates="users",
        uselist=False,
        cascade="all, delete-orphan",
        single_parent=True, 
        passive_deletes=True,
    )
    created_at: Mapped[str] = mapped_column(db.DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[str] = mapped_column(db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


    # I define a new property named password as a function
    @property
    def password(self):
        """ a password property just used for creating the hash version of it """
        raise Exception("password is write-only")

    @password.setter
    def password(self, plain_password):
        self.password_hash = generate_password_hash(plain_password, method="pbkdf2:sha256:600000")

    def check_password(self, password)->bool:
        """ checks it the password would have been able to produce to hash version of it"""
        return check_password_hash(self.password_hash,password)
    
    def get_fullname(self):
        """ returns the fullname of the user"""
        return f"{self.firstname.capitalize()} {self.lastname.capitalize()}"

    def to_dict(self):
        """ represents the information sendable to the client if need be"""
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "is_banned": self.is_banned,
            "role": self.role.value,
            "fullname": self.get_fullname(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            
        }
