from prisma import Prisma
from ...dependencies.password_manager import hash_password
import asyncio
from fastapi import HTTPException, status
from ...utils.models import Register

prisma = Prisma()

async def signup(user_details):
    await prisma.connect()
    queryDetails:Register = dict(user_details)
    hashed_pass = hash_password(user_details.password)
    queryDetails["password"] = hashed_pass

    already_user = await prisma.user.find_first(where={"email":queryDetails["email"]})

    if(already_user):
        await prisma.disconnect()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail="User already exists"
                            )

    await prisma.user.create(
        data = queryDetails
    )
    await prisma.disconnect()

    return

if __name__ == '__main__':
    asyncio.run(signup())