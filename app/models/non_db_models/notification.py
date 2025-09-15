
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import JSON, String, Index
from sqlalchemy.sql import func
try:
    from enum import StrEnum as _StrEnum
except ImportError:
    _StrEnum = enum.Enum
class NotificationStatus(_StrEnum):
    read = 'read'
    unread = 'unread'

class NotificationBase(SQLModel):
    type: str = Field(sa_type=String(50), nullable=False)
    payload: Dict[str, Any] = Field(sa_type=JSON, nullable=False)
    status: NotificationStatus = Field(default=NotificationStatus.unread, nullable=False)
