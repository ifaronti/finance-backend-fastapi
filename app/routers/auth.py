from pydantic import BaseModel
from fastapi import APIRouter, Depends, status, Request
from ..controllers.auth.signup import signup
from ..controllers.auth.login import logon
from ..controllers.auth.oauth import github_login
from ..controllers.auth.user_update import update_user
from ..dependencies.token import verify_token
from ..utils.models import Register, Login, LoginResponse, UserUpdate
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import Annotated

class signup_response(BaseModel):
    Success:bool
    Message:str

router = APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def register(user_details:Register):
    return signup(user_details)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
def login(data:Annotated[Login, Depends(OAuth2PasswordRequestForm)]):
    return logon(data)

@router.get("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
def gitLogin(code:str):
    return github_login(code)

@router.patch("/user")
def user_update(details:Annotated[UserUpdate, Depends(verify_token)], req:Request):
    return update_user(details=details, req=req)
