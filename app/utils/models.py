from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from fastapi import Request

class Register(BaseModel):
    name:str
    password:str
    email:str

class Login(BaseModel):
    username:EmailStr
    password:str

class LoginResponse(BaseModel):
    name:str
    success:bool
    accessToken:str

class TokenPayload(BaseModel):
    exp:datetime
    userId:str

class GitToken(BaseModel):
    access_token:str

class GitUser(BaseModel):
    id:int
    name:str
    avatar_url:str
    email: Optional[EmailStr] = None

    class Config:
        from_attributes=True
        

class Transactions(BaseModel):
    success:bool
    data:str

class CreateBudget(BaseModel):
    categoryId:int
    category:str
    maximum:int
    theme:str
    userId:Optional[int | str] = None


class GenericResponse(BaseModel):
    success:bool
    message:str

class UpdateBudget(BaseModel):
    theme:str
    maximum:int
    budgetId:int
    category:str
    categoryId:int
    spent:int

class CreatePot(BaseModel):
    name:str
    target:int
    total:int
    theme:str

class UpdatePot(BaseModel):
    name:str
    theme:str
    total:int
    target:int
    potId:int

class CreateBill(BaseModel):
    amount:int
    name:str
    avatar:str
    category:str
    categoryId:int