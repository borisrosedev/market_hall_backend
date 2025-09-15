import uuid, enum
from typing import Optional
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime, timezone

# Shared properties
class CartBase(SQLModel):
    created_at: datetime = Field(default=datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default=datetime.now(timezone.utc))
   

class CartCreate(CartBase):
    created_at: datetime = Field(default=datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default=datetime.now(timezone.utc), nullable=False)

class CartUpdate(CartBase):
    updated_at: datetime = Field(default=datetime.now(timezone.utc), nullable=False)


# Properties to return via API, id is always required
class CartPublic(CartBase):
    id: uuid.UUID
    user_id: uuid.UUID