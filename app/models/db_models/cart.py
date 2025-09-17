#from __future__ import annotations 

 
import uuid 
from typing import TYPE_CHECKING, List,Optional
from sqlmodel import Field, Relationship
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from ..non_db_models.cart import CartBase
from .user import User   
#if TYPE_CHECKING: 
from .cart_product import CartProduct
from sqlalchemy import  func ,ColumnDefault

class Cart(CartBase, table=True):
    __tablename__ = "carts"
 
    id: Optional[uuid.UUID]  = Field( 
        default_factory=uuid.uuid4,
        primary_key=True,
        sa_type=PG_UUID(as_uuid=True) 
    ) 

    user_id: uuid.UUID = Field(
        sa_column=Column(
            PG_UUID(as_uuid=True),
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
            index=True,
        )
    )

    user: User = Relationship(
        back_populates="cart",
        sa_relationship_kwargs={
            "passive_deletes": True,  # on delete cascade db side
        },
    )

    
    items: list[CartProduct] = Relationship(
        back_populates="cart",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan", 
            "passive_deletes": True,
        },
    )
