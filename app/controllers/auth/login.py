from fastapi import HTTPException, status
from prisma import Prisma
from ...dependencies.token import create_token
from ...dependencies.password_manager import verify_password
from ...utils.models import Login


prisma=Prisma()

not_found = HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="User not found")

invalid_credentials = HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                    detail="Invalid credentials")

unknown_error = HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                           detail="Unknown error occured; try again")

async def logon(auth_details:Login)->dict:
    await prisma.connect()

    try:
        user = await prisma.user.find_first(where={"email":auth_details.username})
    
        if not user:
            raise not_found
        
        isMatch = verify_password(auth_details.password, user.password)

        if not isMatch:
            raise invalid_credentials

        token = create_token(user.id)
        return {"name":user.name, "access_token":token, "success":True, "token_type":"Bearer"}
    
    finally:
        await prisma.disconnect()
