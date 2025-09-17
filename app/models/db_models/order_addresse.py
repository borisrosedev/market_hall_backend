
import uuid
import importlib
from typing import TYPE_CHECKING, List,Optional
from datetime import datetime, timezone
from pydantic import EmailStr
from sqlmodel import Field, Relationship
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from ..non_db_models.order_addresse import OrderAddresseBase

class OrderAddresse(OrderAddresseBase, table=True):
    __tablename__ = 'order_addresses'
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    order_id: uuid.UUID = Field(default=None, sa_column=Column(PG_UUID(as_uuid=True),
                                                               ForeignKey('orders.id',
                                                                ondelete='CASCADE'), 
                                                               index=True, 
                                                               nullable=True))
    order = Relationship(back_populates='orders'
                        , sa_relationship=relationship(
                        lambda: importlib.import_module('app.models.db_models.order').Order,
                        passive_deletes=True))
