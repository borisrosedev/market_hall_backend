
import uuid
import importlib
from typing import TYPE_CHECKING
from datetime import datetime, timezone
from pydantic import EmailStr
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
from typing import Dict, Any, Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import JSON, String, Index, DateTime
from sqlalchemy.sql import func
from ..non_db_models.notification import NotificationBase

class Notification(NotificationBase, table=True):
    __tablename__ = 'notifications'
    id: Optional[uuid.UUID]= Field(default_factory=uuid.uuid4, index=True, primary_key=True)
    user_id: uuid.UUID = Field(default=None, sa_column=Column(PG_UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=True))
    created_at: datetime = Field(sa_type=DateTime(timezone=True), default_factory=func.now, nullable=False)
    read_at: Optional[datetime] = Field(sa_type=DateTime(timezone=True), nullable=True)
    user: Optional['User'] = Relationship(back_populates='notifications')
    __table_args__ = (Index('ix_notifications_user_status_created', 'user_id', 'status', 'created_at'),)

    def set_read_at(self) -> None:
        """Mark as read DB-side-wise"""
        self.read_at = func.now()