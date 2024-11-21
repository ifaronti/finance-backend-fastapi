from prisma import Prisma
from fastapi import Request, HTTPException, status
from typing import Optional

prisma = Prisma()

async def get_budgets(req:Request, skip:Optional[int]=0):
    user_id = req.state.user
    try:
        await prisma.connect()

        budgets = await prisma.budget.find_many(
            where={'userId':user_id},
            include={
                'category_relate':{
                    'include':{
                        'transactions':{
                            "take":3,
                            "order_by":{
                                "date":"desc"
                            },
                        },
                    }
                },
            },
            skip=skip,
            order={'category':'desc'}
        )
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Budget not updated try again")
    finally:
        await prisma.disconnect()
    return {"success":True, "data":budgets}