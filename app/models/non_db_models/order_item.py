import uuid
import importlib
from typing import Optional, TYPE_CHECKING, Dict, Any
from datetime import datetime, timezone
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from sqlalchemy import ForeignKey
from sqlalchemy import JSON
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from sqlalchemy import DateTime, func


class OrderItemBase(SQLModel):
    sku: str = Field(nullable=False)
    product_name: str = Field(nullable=False)
    unit_price_cents: int = Field(nullable=False, default=1)
    quantity: int = Field(nullable=False, default=1)
    subtotal_cents: int = Field(nullable=False)
    tax_cents: int = Field(nullable=False, default=0)
    discount_cents: int = Field(nullable=False, default=0)
    total_cents: int = Field(nullable=False, default=0)
    currency: str = Field(default="EUR", nullable=False)
    variant_json: Optional[Dict[str, Any]] = Field(default=None, sa_type=JSON, nullable=True)
    metadata_json: Optional[Dict[str, Any]] = Field(default=None, sa_type=JSON, nullable=True)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    )
