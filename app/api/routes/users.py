from typing import Optional, Annotated, Literal, Union, Any
from enum import StrEnum
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime, timezone
import re, shutil, uuid, logging
import os
from pathlib import Path as P
from fastapi import FastAPI, Body, Query, Path, Cookie, Response, status, File, UploadFile, Form, HTTPException, Depends
from fastapi import APIRouter
from app.core.config import settings
from app.models.non_db_models.password import UpdatePassword
from app.models.db_models.user import User as DbUser
from app.models.non_db_models.user import UserCreate, UserPublic, UsersPublic, UserPublicMe, UserRegister, UserUpdate, UserUpdateMe
from app.models.non_db_models.message import Message
from app.core.security import get_password_hash, verify_password
from sqlmodel import Session, select
from app.api.deps import (
    CurrentUser,
    CookieCurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from app.utils import generate_new_account_email, send_email
from app.api.crud.users import get_user_by_email, create_user, get_all_users

BASE_DIR = P(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
logging.basicConfig(level=logging.DEBUG)


api_v1_users = APIRouter(
    prefix="/users",
    tags=["users"]
)


class Cookies(BaseModel):
    model_config = {"extra": "forbid"}
    session: str
    session_id: str


class UserRoles(StrEnum):
    user = "user"
    premium = "premium"
    admin = "admin"

class UserDTO(BaseModel):
    id: int
    email: str
    firstname: str
    lastname: str
    photo_name: Optional[str] = None
    role: UserRoles = UserRoles.user.value



# GET ALL : tested✅

@api_v1_users.get("/", response_model=UsersPublic)
async def read_all_users(session: SessionDep):
    db_users = get_all_users(session=session)
    return {"users": db_users }



# CREATE : tested✅

@api_v1_users.post("/", 
    status_code=status.HTTP_201_CREATED,
    summary="Create a user", 
    #dependencies=[Depends(get_current_active_superuser)],
    response_model=Message
)
async def created_user(session: SessionDep, user_in: Annotated[UserCreate, Body(
    openapi_examples={
        "invalid": {
            "summary":"invalid data (missing password)",
            "value": {
                "firstname":"titin",
                "lastname":"milon",
                "email":"tintin@gmail.com"
            }
        }
    }
)]):
    # CRUD PART
    user = get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    user = create_user(session=session, user_create=user_in)
    # ROUTE PART
    if settings.emails_enabled and user_in.email:
        email_data = generate_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
        send_email(
            email_to=user_in.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )

    return {"message": "user created with a cart"}





# Get the current user DTO data

@api_v1_users.get("/me", 
         status_code=status.HTTP_200_OK, 
         summary="read the current user data (dto)",
         response_model=UserPublicMe,
)
async def read_user_me(current_user: CookieCurrentUser):
    """
    Get current user.
    """
    return { "user": current_user}



# Get the current user DTO data
@api_v1_users.get("/me/access-token", 
         status_code=status.HTTP_200_OK, 
         summary="read the current user data (dto)",
         response_model=UserPublicMe,
)
async def read_user_me(current_user: CurrentUser):
    """
    Get current user.
    """
    return { "user": current_user}



@api_v1_users.put(
    "/{user_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=Message,
)
def update_user(
    *,
    session: SessionDep,
    user_id: uuid.UUID,
    user_in: UserUpdate,
) -> Any:
    """
    Update a user.
    """

    db_user = session.get(DbUser, user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    if user_in.email:
        existing_user = get_user_by_email(session=session, email=user_in.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )

    db_user = update_user(session=session, db_user=db_user, user_in=user_in)
    return {"message":"user updated"}



@api_v1_users.patch(
    "/{user_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=Message,
)
def update_user(
    *,
    session: SessionDep,
    user_id: uuid.UUID,
    user_in: UserUpdate,
) -> Any:
    """
    Update a user.
    """

    db_user = session.get(DbUser, user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    if user_in.email:
        existing_user = get_user_by_email(session=session, email=user_in.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )

    db_user = update_user(session=session, db_user=db_user, user_in=user_in)
    return {"message":"user updated"}


@api_v1_users.patch("/me", response_model=UserPublic)
def update_user_me(
    *, session: SessionDep, user_in: UserUpdateMe, current_user: CurrentUser
) -> Any:
    """
    Update own user.
    """
    if user_in.email:
        existing_user = get_user_by_email(session=session, email=user_in.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )
    user_data = user_in.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(user_data)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


@api_v1_users.put("/me", status_code=status.HTTP_200_OK, response_model=None)
async def update_user(
    session: SessionDep, user_in: UserUpdateMe, current_user: CurrentUser,
    response: Response,
    file: Annotated[Optional[UploadFile],File()] = None,
 
):

    user_data = user_in.model_dump(exclude_unset=True)
    if file:
        ext = os.path.splitext(file.filename)[1]
        safe_name = f"{uuid.uuid4().hex}{ext}"
        dest = f"uploads/{safe_name}"

        with open(dest, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # saved = {
        #     "original_name": file.filename,
        #     "stored_name": safe_name,
        #     "content_type": file.content_type,
        #     "size": file.size,
        #     "path": str(dest),
        # }
        user_data.photo_name = safe_name
    current_user.sqlmodel_update(user_data)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return {
        "message":"user updated"
    }


@api_v1_users.patch("/me/password", response_model=Message)
def update_password_me(
    *, session: SessionDep, body: UpdatePassword, current_user: CurrentUser
) -> Any:
    """
    Update own password.
    """
    if not verify_password(body.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect password")
    if body.current_password == body.new_password:
        raise HTTPException(
            status_code=400, detail="New password cannot be the same as the current one"
        )
    password_hash = get_password_hash(body.new_password)
    current_user.password_hash = password_hash
    session.add(current_user)
    session.commit()
    return Message(message="Password updated successfully")



@api_v1_users.get("/{user_id}", response_model=UserPublic)
def read_user_by_id(
    user_id: uuid.UUID, session: SessionDep, current_user: CurrentUser
) -> Any:
    """
    Get a specific user by id.
    """
    user = session.get(DbUser, user_id)
    if user == current_user:
        return user
    if current_user.role.value is not "admin":
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have enough privileges",
        )
    return user


@api_v1_users.delete("/me", response_model=Message)
def delete_user_me(session: SessionDep, current_user: CurrentUser) -> Any:
    """
    Delete own user.
    """
    session.delete(current_user)
    session.commit()
    return Message(message="user deleted")



@api_v1_users.post("/signup", response_model=Message)
def register_user(session: SessionDep, user_in: UserRegister) -> Any:
    """
    Create new user without the need to be logged in.
    """
    user = get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user_create = UserCreate.model_validate(user_in)
    user = create_user(session=session, user_create=user_create)
    return { "message": "user created with a cart"}








