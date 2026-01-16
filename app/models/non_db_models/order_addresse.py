import uuid
import enum
from typing import Optional
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime, timezone

try:
    from enum import StrEnum as _StrEnum
except ImportError:
    _StrEnum = enum.Enum


class TypeOrderAddresses(_StrEnum):
    shipping = "shipping"
    billing = "billing"


class OrderAddresseBase(SQLModel):
    __tablename__ = "order_addresses"
    type: TypeOrderAddresses = Field(nullable=False)
    full_name: str = Field(nullable=False)
    line1: str = Field(nullable=False)
    line2: str = Field(nullable=True)
    city: str = Field(nullable=False)
    postal_code: str = Field(nullable=False)
    country: str = Field(nullable=False)
    phone: str = Field(nullable=True)
