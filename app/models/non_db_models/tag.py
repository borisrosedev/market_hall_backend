import uuid, enum
from typing import Optional
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, func 

# Shared properties
class TagBase(SQLModel):
    name: str = Field(nullable=False)
    #created_at: datetime = Field(default=datetime.now(timezone.utc), nullable=False)
    #updated_at: datetime = Field(default=datetime.now(timezone.utc), nullable=False)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True, onupdate=func.now())
    )

class TagCreate(TagBase):
    #created_at: Optional[datetime] = Field(default=datetime.now(timezone.utc), nullable=False)
    #updated_at: Optional[datetime] = Field(default=datetime.now(timezone.utc), nullable=False)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True, onupdate=func.now())
    )

class TagUpdate(TagBase):
    #updated_at: Optional[datetime] = Field(default=datetime.now(timezone.utc), nullable=False)
    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), nullable=True, onupdate=func.now())
    )