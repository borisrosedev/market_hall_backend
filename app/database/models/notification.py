import enum
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy import String, Enum, ForeignKey, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .user import User
from .. import db


class NotificationStatus(enum.Enum):
    read = "read"
    unread = "unread"

class Notification(db.Model):
    __tablename__ = "notifications"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    payload: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    status: Mapped[NotificationStatus] = mapped_column(
        Enum(NotificationStatus),
        default=NotificationStatus.unread,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    read_at: Mapped[Optional[datetime]] = mapped_column(
        db.DateTime(timezone=True), nullable=True
    )
    user: Mapped["User"] = relationship(back_populates="notifications")
    
    def set_read_at(self) -> None:
        """Marked as read DB-side-wise"""
        self.read_at = func.now()

    __table_args__ = (
        db.Index(
            "ix_notifications_user_status_created",
            "user_id", "status", "created_at"
        ),
    )
