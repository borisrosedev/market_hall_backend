import enum
from typing import List
from datetime import datetime, timezone
from sqlalchemy import String, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from ...database import db


class StatusOrders(enum.Enum):
    created = "created"
    paid = "paid"
    failed = "failed"


class Order(db.Model):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=False,
        index=True,
        nullable=False,
    )
    amounts_cents: Mapped[int] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="EUR", nullable=False)
    status: Mapped[StatusOrders] = mapped_column(Enum(StatusOrders), default=StatusOrders.created)
    created_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "amounts_cents": self.amounts_cents,
            "currency": self.currency,
            "status": self.status.value,
            "created_at": self.created_at,
        }

    def __repr__(self) -> str:
        return f"<Order id={self.id} user_id={self.user_id} amounts_cents={self.amounts_cents} currency={self.currency!r} status={self.status!r}>"
