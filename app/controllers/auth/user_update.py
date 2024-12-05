from ...dependencies.password_manager import hash_password
from fastapi import Request, HTTPException, status
from prisma import Prisma
from ...utils.models import UserUpdate

prisma = Prisma()

async def update_user(req:Request, details:UserUpdate):
    query = {}
    if details.name:
        query["name"] = details.name

    if details.password:
        pass_hashed = hash_password(details.password)
        query["password"] = pass_hashed

    if details.email:
        query["email"] = details.email

    try:
        await prisma.connect()
        await prisma.user.upsert(
            where= {id:req.state.user},
            data={
                "create": query,
                "update":query
            }
        )
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Check your provided data")
    finally:
        await prisma.disconnect()

    return {"success":True, "message":"User Account updated successfully"}