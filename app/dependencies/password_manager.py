from passlib.context import CryptContext

password_manager = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password:str)->str:
    hashed = password_manager.hash(password)
    return hashed

def verify_password(password:str, hashed_password:str)->bool:
    isMatch = password_manager.verify(password, hashed_password)
    return isMatch