from prisma import Prisma
from fastapi import Request, HTTPException, status
from ...utils.models import UpdateBudget

prisma = Prisma()

async def update_budget(data:UpdateBudget, req:Request):
    data_copy = dict(data).copy()
    data_copy["userId"] = req.state.user

    try:
        await prisma.connect()
        await prisma.budget.upsert(
            where={
                "userId":req.state.user, 
                "budgetId":data_copy["budgetId"]
            },
            data={
                    "update":data_copy,
                    "create":data_copy
                },

        )
    # except:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Budget not updated try again")
    
    finally:
        await prisma.disconnect()

    return {"success":True, "message":"Budget updated successfully"}