from collections.abc import Generator
from typing import Annotated, Union
import logging, jwt
import os
from datetime import datetime as dt, timezone
from uuid import UUID, uuid4
from typing_extensions import TypeAlias
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session, create_engine, select

from app.core import security
from app.core.config import settings
from app.models.db_models.user import User
from app.models.non_db_models.user import UserRoles
from app.models.non_db_models.token import TokenPayload
from app.models.non_db_models.cookie import CookiePayload


# I use the logger to verifiy data 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    pool_pre_ping=True,
    future=True,
)

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]



# Helper function to create a unique file name 

def create_unique_filename(filename) -> str:
    name, ext = os.path.splitext(filename)
    unique_id = uuid4().hex
    timestamp = dt.now().strftime('%Y%m%d-%H%M%S')
    unique_name = f"{name}-{timestamp}-{unique_id}{ext}"
    return unique_name


# Helper function to make sure the id is correctly readable
def _coerce_obj_id(raw) -> Union[int, UUID, str]:
    if isinstance(raw, (int, UUID)):
        return raw
    if isinstance(raw, str):
        try:
            return int(raw)
        except ValueError:
            pass
        try:
            return UUID(raw)
        except ValueError:
            pass
        return raw
    return str(raw)





# ℹ️ To do the same as Flask Backend we use the following function
def get_current_user_from_cookie(request: Request, session: SessionDep) -> User:
    token = request.cookies.get(settings.COOKIE_NAME)
    #logging.info("cookies = %s", dict(request.cookies))
    #logging.info("cookie %s=%s", settings.COOKIE_NAME, token)
    if not token:
        raise HTTPException(status_code=401, detail="not authenticated")
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM],
            options={"require": ["sub", "exp", "usr"]},
        )
        token_payload = TokenPayload.model_validate(payload)
        usr_payload = CookiePayload.model_validate(token_payload.usr)
        user_id = _coerce_obj_id(usr_payload.user_id)
        #logging.info(msg=f"✅ payload {user_id}")
   
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token expired")
    except InvalidTokenError as e:
        logging.exception("Invalid JWT: %s", e)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")

    user = session.get(User, ident=user_id) or session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if getattr(user, "is_banned", False):
        raise HTTPException(status_code=400, detail="Inactive user")
    return user



CookieCurrentUser: TypeAlias = Annotated[User, Depends(get_current_user_from_cookie)]








## ----------------------- V2 ---------------------------


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM],
            options={"require": ["sub", "exp"]},
        )
        token_data = TokenPayload.model_validate(payload)  
        sub_payload = CookiePayload.model_validate(token_data.sub)
        user_id = _coerce_obj_id(sub_payload.user_id)
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token expired")
    except (InvalidTokenError, ValidationError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")

    user = session.get(User, user_id) or session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if getattr(user, "is_banned", False):
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

CurrentUser: TypeAlias = Annotated[User, Depends(get_current_user)]




# not yet needed
def get_current_active_superuser(current_user: CurrentUser) -> User:
    # Accepte UserRoles.admin (enum) ou sa valeur string
    role = getattr(current_user, "role", None)
    if role != UserRoles.admin and role != getattr(UserRoles.admin, "value", "admin"):
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have enough privileges",
        )
    return current_user
