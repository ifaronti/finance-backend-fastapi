from prisma import Prisma
from fastapi import HTTPException, status

prisma = Prisma

async def delete_budget(id:int):
    try:
        await prisma.connect()
        await prisma.budget.delete(where={'budgetId':id})
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Budget is not deleted, try again")
    finally:
        await prisma.disconnect()
    return {"success":True, "message":"Budget deleted successfully"}