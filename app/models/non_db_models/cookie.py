import uuid, enum
from typing import Union, Optional
from uuid import UUID
from pydantic import EmailStr, BaseModel
from app.models.non_db_models.user import UserRoles



class CookiePayload(BaseModel):
    user_id: Union[int, str, UUID]
    email: EmailStr
    role: Optional[str] = None
