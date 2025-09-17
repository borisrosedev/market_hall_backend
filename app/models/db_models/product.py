#from __future__ import annotations

import uuid, importlib
from typing import TYPE_CHECKING,Optional
from datetime import datetime, timezone
from sqlmodel import Field, Relationship
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from ..non_db_models.product import ProductBase

#if TYPE_CHECKING:
from .cart_product import CartProduct
from .tag_product import TagProduct


class Product(ProductBase, table=True):
    __tablename__ = "products"

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)

    # # a product belongs to one user (vendor / creator)
    # user_id: uuid.UUID = Field(
    #     default=None,
    #     sa_column=Column(
    #         PG_UUID(as_uuid=True),
    #         ForeignKey("users.id", ondelete="CASCADE"),  
    #         index=True,
    #         nullable=True,)
    # )

    # # points back to the 'products' attribute on User
    # user = Relationship(
    #     back_populates="products",
    #     # sa_relationship_kwargs={"passive_deletes": True},
    #     sa_relationship=relationship( 
    #         lambda: importlib.import_module(
    #             "app.models.db_models.user"
    #         ).User,
    #         passive_deletes=True
    #     )
    # )

    # many-to-many via association table CartProduct
    carts_link: list[CartProduct] = Relationship(
        back_populates="product",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "passive_deletes": True,
        },
    )

    # many-to-many via association table TagProduct
    tags_link: list[TagProduct] = Relationship(
        back_populates="product",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "passive_deletes": True,
        },
    )


    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=True,
    )
