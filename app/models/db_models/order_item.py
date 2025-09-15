
import uuid
from datetime import datetime, timezone
from typing import Optional
import importlib
from pydantic import EmailStr
from sqlmodel import Field, Relationship
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from ..non_db_models.order_item import OrderItemBase

class OrderItem(OrderItemBase, table=True):
    __tablename__ = 'order_items'
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    order_id: uuid.UUID = Field(default=None, sa_column=Column(PG_UUID(as_uuid=True), ForeignKey('orders.id', ondelete='CASCADE'), index=True, nullable=True))
    product_id: uuid.UUID = Field(default=None, sa_column=Column(PG_UUID(as_uuid=True), ForeignKey('products.id', ondelete='CASCADE'), index=True, nullable=True))
    order = Relationship(back_populates='orders', sa_relationship=relationship(lambda: importlib.import_module('app.models.db_models.order').Order, passive_deletes=True))
    product = Relationship(back_populates='products', sa_relationship=relationship(lambda: importlib.import_module('app.models.db_models.product').Product, passive_deletes=True))
