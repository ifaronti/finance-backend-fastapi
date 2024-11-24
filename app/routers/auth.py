from pydantic import BaseModel
from fastapi import APIRouter, Depends, status
from ..controllers.auth.signup import signup
from ..controllers.auth.login import logon
from ..controllers.auth.oauth import github_login
from ..utils.models import Register, Login, LoginResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import Annotated


class signup_response(BaseModel):
    Success:bool
    Message:str

router = APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=signup_response)
async def register(user_details:Register):
    await signup(user_details)
    return {"Success":True, "Message":"User created successfully"}


@router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def login(data:Annotated[Login, Depends(OAuth2PasswordRequestForm)]):
    return await logon(data)

@router.get("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def gitLogin(code:str):
    return await github_login(code)