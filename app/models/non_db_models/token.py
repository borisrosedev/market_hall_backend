import uuid, enum
from typing import Optional, Any
from pydantic import BaseModel, EmailStr
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime, timezone
from app.models.non_db_models.cookie import CookiePayload


# JSON payload containing access token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    usr: CookiePayload
    exp: int
    iat: int | None = None
    nbf: int | None = None
