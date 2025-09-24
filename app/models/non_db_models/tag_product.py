
import uuid, enum
from typing import Optional
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime, timezone


class TagProductBase(SQLModel):
    pass