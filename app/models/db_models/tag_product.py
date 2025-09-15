#from __future__ import annotations 

import uuid, importlib
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from ..non_db_models.tag_product import TagProductBase

# if TYPE_CHECKING:
#     from .tag import Tag
#     from .product import Product


class TagProduct(TagProductBase, table=True):
    __tablename__ = "tag_products"

    tag_id: uuid.UUID = Field(
        sa_column=Column(
            PG_UUID(as_uuid=True),
            ForeignKey("tags.id", ondelete="CASCADE"),
            primary_key=True,
            index=True,
            nullable=False,
        )
    )

    product_id: uuid.UUID = Field(
        sa_column=Column(
            PG_UUID(as_uuid=True),
            ForeignKey("products.id", ondelete="CASCADE"), 
            primary_key=True,
            index=True,
            nullable=False,
        )
    )

    tag = Relationship(
        back_populates="products_link",
        #sa_relationship_kwargs={"passive_deletes": True},
        sa_relationship=relationship( 
            lambda: importlib.import_module(
                "app.models.db_models.tag"
            ).Tag,
            passive_deletes=True
        )
    )
    product = Relationship(
        back_populates="tags_link",
        #sa_relationship_kwargs={"passive_deletes": True},
        sa_relationship=relationship( 
            lambda: importlib.import_module(
                "app.models.db_models.product"
            ).Product,
            passive_deletes=True
        )
    )
