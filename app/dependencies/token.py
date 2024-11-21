import jwt
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from ..utils.config import Settings
from fastapi import HTTPException, status, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from ..utils.models import TokenPayload

class CreateToken(BaseModel):
    exp:datetime
    userId:int

settings = Settings()

time = settings.TOKEN_TIME

error_code = HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED,
                           detail="Token not created, try again")

invalid_credentials = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                    detail="Invalid credentials provided")

token_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_token(id:int)->str:
    data = {"user_id":id}
    expire = datetime.now(timezone.utc) + timedelta(days=settings.TOKEN_EXPIRY)
    data.update({"exp":expire})

    try:
        token = jwt.encode(data, settings.JWT_SECRET, settings.ALGORITHM)
    
    except jwt.exceptions.PyJWTError:
        raise error_code

    return token

def verify_token(token:Annotated[str, Depends(token_scheme)], req:Request):
    try:
        payload:TokenPayload = jwt.decode(token, settings.JWT_SECRET, settings.ALGORITHM)

    except jwt.exceptions.ExpiredSignatureError:
        raise invalid_credentials
    
    except jwt.exceptions.ImmatureSignatureError:
        raise invalid_credentials
    
    except jwt.exceptions.InvalidAlgorithmError:
        raise invalid_credentials
    
    except jwt.exceptions.DecodeError:
        raise invalid_credentials
    
    except jwt.exceptions.InvalidKeyError:
        raise invalid_credentials
    
    except jwt.exceptions.PyJWTError:
        raise error_code
    
    req.state.user = dict(payload)["user_id"]
    print(req.state.user)