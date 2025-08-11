# models/tag_product.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Index
from .. import db

class TagProduct(db.Model):
    __tablename__ = "tag_products"

    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        primary_key=True,
    )

    # ✅ back_populates appariés aux noms ci-dessus
    tag: Mapped["Tag"] = relationship(back_populates="products_link")
    product: Mapped["Product"] = relationship(back_populates="tag_links")

    __table_args__ = (
        Index("ix_tag_products_tag", "tag_id"),
        Index("ix_tag_products_product", "product_id"),
    )

    def __repr__(self) -> str:
        return f"<TagProduct tag_id={self.tag_id} product_id={self.product_id}>"
