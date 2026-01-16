import uuid, enum
from typing import Optional
from pydantic import EmailStr, BaseModel, field_validator
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime, timezone


# Shared properties
class ProductBase(SQLModel):
    description: str = Field(nullable=False)
    sku: str = Field(nullable=False)
    quantity: int = Field(nullable=False)
    price_cents: int = Field(nullable=False, gt=0)
    is_available: bool = Field(default=True, nullable=False)
    published: bool = Field(default=False, nullable=False)
    name: str = Field(nullable=False)
    photo_name: str = Field(nullable=True)


class ProductDTO(ProductBase):
    pass


class ProductDTOResponse(BaseModel):
    product: ProductDTO


class ProductCreateRequest(ProductBase):
    @field_validator("description", "sku", "name")
    @classmethod
    def _strip_optional(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if isinstance(v, str) else v
