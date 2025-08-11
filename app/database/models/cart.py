from typing import List
from sqlalchemy import Integer, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .. import db

class Cart(db.Model):
    """ A class that represents the User Cart"""
    __tablename__="carts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,          
        index=True,
        nullable=False,
    )

    # cart will be a virtual field when querying a user 
    user: Mapped["User"] = relationship(back_populates="cart")


    items: Mapped[List["CartProduct"]] = relationship(
        back_populates="cart",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    products: Mapped[List["Product"]] = relationship(
        secondary="cart_products",
        viewonly=True,
        lazy="dynamic",
    )

    created_at: Mapped[str] = mapped_column(db.DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[str] = mapped_column(db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    def to_dict(self) -> dict:
        """ serialize the cart record"""
        return {
        "id": self.id,
        "user_id": self.user_id,
        "created_at": self.created_at,
        "updated_at": self.updated_at,
        "items": [
            {
                "id": it.id,
                "name": it.name if it.name else None,
                "photo_name": it.photo_name,
                "quantity": it.quantity,
            }
            for it in self.items
        ],
    }



    def __repr__(self) -> str:
        return f"<Cart id={self.id} user_id={self.user_id}>"
