from prisma import Prisma
from fastapi import status, HTTPException

prisma = Prisma()

prisma_exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="An error occured check id params")


async def delete_pot(id:int):
    try:
        await prisma.connect()
        await prisma.pot.delete(where={"potId":id})
    except:
        raise prisma_exception
    finally:
        await prisma.disconnect()

    return {"success":True, "message":"Pot deleted"}