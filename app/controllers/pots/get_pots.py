from prisma import Prisma
from fastapi import Request, status, HTTPException
from typing import Optional


prisma = Prisma()

prisma_exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="An error occured check id params")

async def get_pots(req:Request, skip:Optional[int]=0):
    user_id = req.state.user
    try:
        await prisma.connect()
        pots = await prisma.pots.find_many(where={'userId':user_id}, skip=skip, take=10)
    except:
        raise prisma_exception
    finally:
        await prisma.disconnect()

    return {"success":True, "data":list(pots)}