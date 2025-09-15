
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

class StatusOrders(_StrEnum):
    created = 'created'
    paid = 'paid'
    failed = 'failed'

class OrderBase(SQLModel):
    amounts_cents: int = Field(nullable=False)
    currency: str = Field(default='EUR', nullable=False)
    status: StatusOrders = Field(default=StatusOrders.created)
    created_at: datetime = Field(default=datetime.now(timezone.utc), nullable=False)

class OrderCreate(OrderBase):
    created_at: Optional[datetime] = Field(default=datetime.now(timezone.utc), nullable=False)

