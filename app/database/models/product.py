from datetime import datetime, timezone
from sqlalchemy import String, Enum, Boolean, DATETIME, func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List
from .. import db


class Product(db.Model):
    """ Product """
    __tablename__="products"
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    is_available: Mapped[bool] = mapped_column(default=False, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    photo_name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[str] = mapped_column(db.DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[str] = mapped_column(db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    
    carts_link: Mapped[List["CartProduct"]] = relationship(
        back_populates="product",
        passive_deletes=True,
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id, 
            "description": self.description,
            "is_available": self.is_available,
            "name": self.name,
            "photo_name": self.photo_name,
            "price": self.price, 
            "quantity": self.quantity,
            "created_at": self.created_at,
            "updated_at": self.updated_at

        }

    def __repr__(self) -> str:
        return f"<Product id={self.id} name={self.name!r}>"






