from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ALGORITHM:str
    JWT_SECRET:str
    TOKEN_EXPIRY:int
    TOKEN_TIME:str
    CLIENT_ID:str
    CLIENT_SECRET:str
