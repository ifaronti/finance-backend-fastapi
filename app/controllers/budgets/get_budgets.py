from prisma import Prisma
from fastapi import Request, HTTPException, status
from typing import Optional

prisma = Prisma()

async def get_budgets(req:Request, skip:Optional[int]=0):
    try:
        await prisma.connect()

        budgets = await prisma.query_raw (f""" 
            WITH recent_transactions AS (
                SELECT 
                    t."categoryId", 
                    t.name, 
                    t.amount, 
                    t.date, 
                    t.avatar,
                    ROW_NUMBER() OVER (PARTITION BY t."categoryId" ORDER BY t.date DESC) AS row_num
                FROM transactions t
                WHERE EXTRACT(MONTH FROM t.date) > 7  -- Filter transactions after July
                AND t."userId" = '{req.state.user}'
            )
            SELECT 
                bg."budgetId", 
                bg.maximum, 
                bg.category, 
                bg."isPlaceholder", 
                bg."categoryId", 
                SUM(t.amount) AS spent, 
                bg.theme, 
                json_agg(
                    json_build_object(
                        'name', t.name, 
                        'amount', t.amount, 
                        'date', t.date, 
                        'avatar', t.avatar
                    )
                ) AS transactions
            FROM 
                budgets bg
            LEFT JOIN recent_transactions t 
                ON bg."categoryId" = t."categoryId"
                AND t.row_num <= 3  -- Only join the top 3 most recent transactions per category
            WHERE 
                bg."userId" = '{req.state.user}'
            GROUP BY 
                bg."budgetId" """)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Budget not updated try again")
    finally:
        await prisma.disconnect()
    return {"success":True, "data":budgets}