#from __future__ import annotations

import uuid
from datetime import datetime, timezone
#from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship
from sqlalchemy import UniqueConstraint
from ..non_db_models.tag import TagBase
from typing import List,Optional

#if TYPE_CHECKING:
from .tag_product import TagProduct


class Tag(TagBase, table=True):
    __tablename__ = "tags"
    __table_args__ = (
        UniqueConstraint("name", name="uq_tags_name"), 
    )

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True, max_length=64)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=True
    )

    products_link: list[TagProduct] = Relationship(
        back_populates="tag",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "passive_deletes": True,
        },
    )

    def __repr__(self) -> str:
        return f"Tag(id={self.id}, name={getattr(self, 'name', None)!r})"
