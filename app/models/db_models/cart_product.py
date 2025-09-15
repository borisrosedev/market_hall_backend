import uuid, importlib
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from ..non_db_models.cart_product import CartProductBase

#if TYPE_CHECKING:
##from .product import Product


class CartProduct(CartProductBase, table=True):
    __tablename__ = "cart_products"

    # composite primary key
    cart_id: uuid.UUID = Field(
        sa_column=Column(
            PG_UUID(as_uuid=True),
            ForeignKey("carts.id", ondelete="CASCADE"),
            primary_key=True,
            index=True,
        )
    )
    product_id: uuid.UUID = Field(
        sa_column=Column(
            PG_UUID(as_uuid=True),
            ForeignKey("products.id", ondelete="CASCADE"),
            primary_key=True,
            index=True,
        )
    )

    cart = Relationship(
        back_populates="items",
        #sa_relationship_kwargs={"passive_deletes": True},
        sa_relationship=relationship( 
            lambda: importlib.import_module(
                "app.models.db_models.cart"
            ).Cart,
            passive_deletes=True
        )
    )
    product = Relationship(
        back_populates="carts_link",
        #sa_relationship_kwargs={"passive_deletes": True},
        sa_relationship=relationship( 
            lambda: importlib.import_module(
                "app.models.db_models.product"
            ).Product,
            passive_deletes=True
        )
    )
