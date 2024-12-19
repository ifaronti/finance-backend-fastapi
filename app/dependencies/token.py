import jwt
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from ..utils.config import Settings
from fastapi import HTTPException, status, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from ..utils.models import TokenPayload
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class CreateToken(BaseModel):
    exp:datetime
    userId:int

settings = Settings()

time = settings.TOKEN_TIME

error_code = HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED,
                           detail="Token not created, try again")

invalid_credentials = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                    detail="Invalid credentials provided")

token_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login",)


def create_token(id:int)->str:
    data = {"user_id":id}
    expire = datetime.now(timezone.utc) + timedelta(days=settings.TOKEN_EXPIRY)
    data.update({"exp":expire})

    try:
        token = jwt.encode(data, settings.JWT_SECRET, settings.ALGORITHM)
    
    except jwt.exceptions.PyJWTError:
        logging.error("PyJWTError error:%s", token)
        raise error_code

    return token

def verify_token(token:Annotated[str, Depends(token_scheme)], req:Request):
    try:
        payload:TokenPayload = jwt.decode(token, settings.JWT_SECRET, settings.ALGORITHM)

    except jwt.exceptions.ExpiredSignatureError:
        print(jwt.exceptions.ExpiredSignatureError)
        logging.error("ExpiredSignatureError error:%s", token)
        raise invalid_credentials
    
    except jwt.exceptions.ImmatureSignatureError:
        print(jwt.exceptions.ImmatureSignatureError)
        logging.error("ImmatureSignatureError error:%s", token)
        raise invalid_credentials
    
    except jwt.exceptions.InvalidAlgorithmError:
        print(jwt.exceptions.InvalidAlgorithmError)
        logging.error("InvalidAlgorithmError error:%s", token)
        raise invalid_credentials
    
    except jwt.exceptions.DecodeError:
        print(jwt.exceptions.DecodeError)
        raise invalid_credentials
    
    except jwt.exceptions.InvalidKeyError:
        print(jwt.exceptions.InvalidKeyError)
        logging.error("InvalidKeyError error:%s", token)
        raise invalid_credentials
    
    except jwt.exceptions.PyJWTError:
        logging.error("PyJWTError error:%s", token)
        print(jwt.exceptions.PyJWTError)
        raise error_code
    except Exception:
        logging.error("Exception error:%s", token)
        print(Exception)
        raise Exception
    
    req.state.user = dict(payload)["user_id"]