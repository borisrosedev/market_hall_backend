from __future__ import annotations

import uuid
import enum
from typing import Optional

from pydantic import EmailStr, SecretStr, ConfigDict, field_validator
from sqlmodel import SQLModel, Field


try:
    from enum import StrEnum as _StrEnum
except ImportError: 
    _StrEnum = enum.Enum

class UserRoles(_StrEnum): 
    user = "user"
    premium = "premium"
    admin = "admin"



class UserBase(SQLModel):
    """
    Shared business fields
    """
    model_config = ConfigDict(from_attributes=True) 

    firstname: str = Field(min_length=1, max_length=50)
    lastname: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=255)
    is_banned: bool = Field(default=False)
    photo_name: Optional[str] = Field(default=None, max_length=255)
    role: UserRoles = Field(default=UserRoles.user)

    @field_validator("firstname", "lastname")
    @classmethod
    def _strip_and_basic_check(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("the field cannot be empty")
        return v


class UserCreate(UserBase):
    """
    creational schema: inherit from UserBase and add a plain password that won't be stocked.
    """
    password: SecretStr = Field(min_length=8, max_length=128)


class UserRegister(SQLModel):
    """
    minimal variant registering via email and password only
    """
    email: EmailStr = Field(max_length=255)
    password: SecretStr = Field(min_length=8, max_length=128)


class UserUpdate(SQLModel):
    """
    PATCH partiel (all fields are optional).
    """
    firstname: Optional[str] = Field(default=None, min_length=1, max_length=50)
    lastname: Optional[str] = Field(default=None, min_length=1, max_length=50)
    email: Optional[EmailStr] = Field(default=None, max_length=255)
    photo_name: Optional[str] = Field(default=None, max_length=255)
    password: Optional[SecretStr] = Field(default=None, min_length=8, max_length=128)
    role: Optional[UserRoles] = None
    is_banned: Optional[bool] = None

    @field_validator("firstname", "lastname")
    @classmethod
    def _strip_optional(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if isinstance(v, str) else v


class UserUpdateMe(SQLModel):
    """
    partial PATCH/PUT without is_banned 
    """
    firstname: Optional[str] = Field(default=None, min_length=1, max_length=50)
    lastname: Optional[str] = Field(default=None, min_length=1, max_length=50)
    email: Optional[EmailStr] = Field(default=None, max_length=255)
    photo_name: Optional[str] = Field(default=None, max_length=255)
    password: Optional[SecretStr] = Field(default=None, min_length=8, max_length=128)
    role: Optional[UserRoles] = Field(default=None)
    @field_validator("firstname", "lastname")
    @classmethod
    def _strip_optional(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if isinstance(v, str) else v


class UserPublic(UserBase):
    """
    output schema includes id
    """
    id: uuid.UUID

class UserPublicMe(SQLModel):
    user: UserPublic


class UsersPublic(SQLModel):
    """
    aggregated list
    """
    users: list[UserPublic]

