
import uuid
import importlib
from typing import TYPE_CHECKING
from datetime import datetime, timezone
from pydantic import EmailStr
from sqlmodel import Field, Relationship
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from ..non_db_models.order import OrderBase

class Order(OrderBase, table=True):
    __tablename__ = 'orders'
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
    user_id: uuid.UUID = Field(default=None, 
                            sa_column=Column(PG_UUID(as_uuid=True),
                            ForeignKey('users.id', ondelete='CASCADE'), 
                            index=True, 
                            nullable=True))
    user = Relationship(back_populates='orders'
                        , sa_relationship=relationship(
                        lambda: importlib.import_module('app.models.db_models.user').User
                        , passive_deletes=True))
    