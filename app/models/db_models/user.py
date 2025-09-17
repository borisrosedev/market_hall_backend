#from __future__ import annotations

import uuid
from datetime import datetime, timezone
#from typing import TYPE_CHECKING
import importlib
from pydantic import EmailStr
from sqlmodel import Field, Relationship
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String 
from ..non_db_models.user import UserBase
from typing import List,Optional
from sqlalchemy import Column, DateTime, func 
#if TYPE_CHECKING:
    #from .cart import Cart


class User(UserBase, table=True):
    __tablename__ = "users"

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)


    email: EmailStr = Field(
        sa_column=Column(
            String(255),
            unique=True,  
            index=True,    
            nullable=False
        )
    )

    password_hash: str = Field(nullable=False)


    cart = Relationship(
    #     back_populates="user",
    #     sa_relationship_kwargs={
    #         "uselist": False,
    #         "single_parent": True,        
    #         "cascade": "all, delete-orphan",
    #     },
        sa_relationship=relationship(
            lambda: importlib.import_module(
                "app.models.db_models.cart"
            ).Cart,
            back_populates="user",
            uselist=False,
            single_parent=True,
            cascade="all, delete-orphan",
        )
    )

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True, onupdate=func.now())
    )
    notifications: List['Notification'] = Relationship(back_populates='user')

    def get_fullname(self) -> str:
        first = (self.firstname or "").strip().capitalize()
        last = (self.lastname or "").strip().capitalize()
        return f"{first} {last}".strip()
