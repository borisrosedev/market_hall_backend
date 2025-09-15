import uuid, enum
from typing import Optional
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime, timezone

# Shared properties
class TagBase(SQLModel):
    name: str = Field(nullable=False)
    created_at: datetime = Field(default=datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default=datetime.now(timezone.utc), nullable=False)


class TagCreate(TagBase):
    created_at: Optional[datetime] = Field(default=datetime.now(timezone.utc), nullable=False)
    updated_at: Optional[datetime] = Field(default=datetime.now(timezone.utc), nullable=False)

class TagUpdate(TagBase):
    updated_at: Optional[datetime] = Field(default=datetime.now(timezone.utc), nullable=False)
