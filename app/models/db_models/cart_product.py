from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, CheckConstraint, Index
from ...database import db


class CartProduct(db.Model):
    """Product in the Cart"""

    __tablename__ = "cart_products"

    cart_id: Mapped[int] = mapped_column(
        ForeignKey("carts.id", ondelete="CASCADE"),
        primary_key=True,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        primary_key=True,
    )

    quantity: Mapped[int] = mapped_column(default=1, nullable=False)
    cart: Mapped["Cart"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship(back_populates="carts_link")

    __table_args__ = (
        CheckConstraint("quantity >= 0", name="ck_cart_products_quantity_non_negative"),
        Index("ix_cart_products_cart", "cart_id"),
        Index("ix_cart_products_product", "product_id"),
    )

    def __repr__(self) -> str:
        return (
            f"<CartProduct cart_id={self.cart_id} product_id={self.product_id} qty={self.quantity}>"
        )
