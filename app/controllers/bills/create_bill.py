from fastapi import Request, HTTPException, status
from prisma import Prisma
from ...utils.models import CreateBill

prisma = Prisma()

prisma_exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="An error occured")

async def create_bill(data:CreateBill, req:Request):
    data_copy = dict(data).copy()
    data_copy["userId"] = req.state.user
    try:
        await prisma.connect()
        await prisma.bills.create(data=data_copy)
    except:
        raise prisma_exception
    finally:
        await prisma.disconnect()

    return {"success":True, "message":"Bill successfully added to account"}