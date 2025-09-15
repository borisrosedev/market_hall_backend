from typing import  Annotated
from fastapi import FastAPI, Body, Query, Path, Cookie, Response, status, File, UploadFile, Form, HTTPException, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from app.api.deps import SessionDep
from datetime import timedelta, datetime, timezone
from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.api.crud.users import get_password_hash,get_user_by_email, create_user
from app.api.crud.auth import authenticate
from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.non_db_models.message import Message 
from app.models.non_db_models.password import NewPassword
from app.models.non_db_models.token import Token
from app.models.non_db_models.user import UserPublic
from app.utils import (
    generate_password_reset_token,
    generate_reset_password_email,
    send_email,
    verify_password_reset_token,
)



api_v1_auth = APIRouter(
    tags=["auth"],
    prefix="/auth"
)



class LoginRequest(BaseModel):
    email: str 
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "boris@gmail.com",
                    "password": "caroline123",
                },
                {
                    "email":"alexandre@gmail.com",
                    "password":"ludivine123"
                }
            ]
        }
    }



@api_v1_auth.post("/login")
def login_access_token(
    response: Response,
    session: SessionDep,
    email: EmailStr = Body(),
    password: str = Body(min_length=8),
):
    user = authenticate(session=session, email=email, password=password)
    if not user:
        raise HTTPException(status_code=400, detail="invalid data")

     
    expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = security.create_access_token(subject={"email":user.email, "user_id": user.id, "role": user.role.value},expires_delta=expires)

    now = datetime.now(timezone.utc)
    response.set_cookie(
        key=settings.COOKIE_NAME,
        value=token,
        httponly=True,
        secure=settings.COOKIE_SECURE,        
        samesite=settings.COOKIE_SAMESITE,     
        max_age=int(expires.total_seconds()),
        expires=int((now + expires).timestamp()),
        domain=settings.COOKIE_DOMAIN or None,
        path=settings.COOKIE_PATH,
    )
    return {"message": "session start"}


@api_v1_auth.get("/logout")
def logout(response: Response):
    response.delete_cookie(
        key=settings.COOKIE_NAME,
        domain=settings.COOKIE_DOMAIN,
        path=settings.COOKIE_PATH,
    )
    return {"message": "session end"}





















## ADDITIONAL FEATURE : TOKEN-ACCESS

@api_v1_auth.post("/login/test-token", response_model=UserPublic)
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user



@api_v1_auth.post("/login/access-token")
def login_access_token_without_cookie(
    session: SessionDep, 
    email: Annotated[EmailStr, Body()],
    password: Annotated[
    str, Body(
        min_length=8, 
        examples=[{"password":"poisonivy123"}]
    )]) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = authenticate(
        session=session, email=email, password=password
    )
    if not user:
        raise HTTPException(status_code=400, detail="invalid data")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )









##------------------ V2 -------------------------



@api_v1_auth.post("/password-recovery/{email}")
def recover_password(email: str, session: SessionDep) -> Message:
    """
    Password Recovery
    """
    user = get_user_by_email(session=session, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    email_data = generate_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    send_email(
        email_to=user.email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return Message(message="password recovery email sent")




# to add in the official backend
@api_v1_auth.post("/reset-password/")
def reset_password(session: SessionDep, body: NewPassword) -> Message:
    """
    Reset password
    """
    email = verify_password_reset_token(token=body.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = get_user_by_email(session=session, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    password_hash = get_password_hash(password=body.new_password)
    user.password_hash = password_hash
    session.add(user)
    session.commit()
    return Message(message="password updated")






# to add in the official backend
@api_v1_auth.post(
    "/password-recovery-html-content/{email}",
    dependencies=[Depends(get_current_active_superuser)],
    response_class=HTMLResponse,
)
def recover_password_html_content(email: str, session: SessionDep) -> Any:
    """
    HTML Content for Password Recovery
    """
    user = get_user_by_email(session=session, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    email_data = generate_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )

    return HTMLResponse(
        content=email_data.html_content, headers={"subject:": email_data.subject}
    )