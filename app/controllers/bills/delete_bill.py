from fastapi import HTTPException, Request, status
from prisma import Prisma

prisma = Prisma()

prisma_exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="An error occured")

async def delete_bill(id:int, req:Request):
    try:
        await prisma.connect()
        await prisma.bills.delete(where={'BillId':id, "userId":req.state.user})
    except:
        raise prisma_exception
    finally:
        await prisma.disconnect()

    return {"success":True, "message":"Bill deleted successfully"}