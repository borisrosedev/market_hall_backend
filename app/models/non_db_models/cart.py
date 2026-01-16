import uuid, enum
from typing import Optional
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


# Shared properties
class CartBase(SQLModel):
    # created_at: datetime = Field(default=datetime.now(timezone.utc), nullable=False)
    # updated_at: datetime = Field(default=datetime.now(timezone.utc))
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
        ),
    )

    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
            onupdate=func.now(),
            server_default=func.now(),
        ),
    )


class CartCreate(CartBase):
    ccreated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),  # Généré par PostgreSQL
        ),
    )

    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
            onupdate=func.now(),
            server_default=func.now(),
        ),
    )

    # created_at: datetime = Field(default=datetime.now(timezone.utc), nullable=False)
    # updated_at: datetime = Field(default=datetime.now(timezone.utc), nullable=False)


class CartUpdate(CartBase):
    # updated_at: datetime = Field(default=datetime.now(timezone.utc), nullable=False)
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
            onupdate=func.now(),
            server_default=func.now(),
        ),
    )


# Properties to return via API, id is always required
class CartPublic(CartBase):
    id: uuid.UUID
    user_id: uuid.UUID
