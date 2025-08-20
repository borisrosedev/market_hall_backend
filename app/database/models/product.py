# models/product.py
from typing import List
from datetime import datetime, timezone
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from .. import db

class Product(db.Model):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    published: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_available: Mapped[bool] = mapped_column(default=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    photo_name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    tag_links: Mapped[List["TagProduct"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    tags = association_proxy("tag_links", "tag")

    carts_link: Mapped[List["CartProduct"]] = relationship(
            back_populates="product",
            passive_deletes=True,
    )
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "description": self.description,
            "published": self.published,
            "is_available": self.is_available,
            "name": self.name,
            "photo_name": self.photo_name,
            "price": self.price,
            "quantity": self.quantity,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "tags": [
                {
                    "id": link.tag.id,
                    "name": link.tag.name
                }
                for link in self.tag_links
            ],
        }

    def __repr__(self) -> str:
        return f"<Product id={self.id} name={self.name!r} description={self.description!r} photo_name={self.photo_name!r} price={self.price} quantity={self.quantity}>"
