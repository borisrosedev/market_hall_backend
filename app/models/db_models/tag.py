# models/tag.py
from typing import List
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ...database import db

class Tag(db.Model):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    products_link: Mapped[List["TagProduct"]] = relationship(
        back_populates="tag",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,  
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "products_link": [
                {
                    "product_id": link.product_id,
                    "quantity": link.quantity,
                    "product": {
                        "id": link.product.id,
                        "name": link.product.name,
                        "photo_name": link.product.photo_name,
                        "price_cents": link.product.price_cents,
                    },
                }
                for link in self.products_link
            ],
        }

    def __repr__(self) -> str:
        return f"<Tag id={self.id} name={self.name}>"
