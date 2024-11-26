from prisma import Prisma
from fastapi import status, HTTPException, Request
from ...utils.models import CreatePot


prisma = Prisma()

prisma_exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="An error occured; resource not created; check payload")

async def create_pot(data:CreatePot, req:Request):
    data_copy = dict(data).copy()
    data_copy["userId"] = req.state.user
    try:
        await prisma.connect()
        await prisma.pots.create(data=data_copy)
    except:
        raise prisma_exception
    finally:
        await prisma.disconnect()

    return {"success":True, "message": "Pot created successfully"}