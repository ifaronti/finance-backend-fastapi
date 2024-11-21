from prisma import Prisma
from ...utils.models import CreateBudget
from fastapi import Request, HTTPException, status
from datetime import datetime

prisma = Prisma()

async def create_budget(data:CreateBudget, req:Request):
    user_id = req.state.user
    data_copy = dict(data).copy()
    data_copy["userId"] = user_id

    try:
        await prisma.connect()
        total_spent = await prisma.transactions.group_by(
            by=["userId"],
            where={
                "userId":user_id, 
                "category":data_copy["category"],
                "date":{
                    "gte":"2024-08-31T20:50:18Z",
                }
            },
            sum={
                "amount":True
            }
        )
        if len(total_spent) == 0:
            spent = 0

        data_copy["spent"] = spent
        await prisma.budget.create(
            data=data_copy,
        )
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error occured")
    finally:
        await prisma.disconnect()
        
    return {"success":True, "Message": "Budget created successfully"}