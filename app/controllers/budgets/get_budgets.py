from fastapi import Request, HTTPException, status
from typing import Optional
from ...pyscopg_connect import dbconnect

async def get_budgets(req:Request, skip:Optional[int]=0):
    cursor = dbconnect.cursor()
    try:
        sql = f""" 
            WITH recent_transactions AS (
                SELECT 
                    t."categoryId", 
                    t.name, 
                    t.amount, 
                    t.date, 
                    t.avatar,
                    ROW_NUMBER() OVER (PARTITION BY t."categoryId" ORDER BY t.date DESC) AS row_num
                FROM transactions t
                WHERE t."userId" = '{req.state.user}'
            )
            SELECT 
                bg."budgetId", 
                bg.maximum, 
                bg.category, 
                bg."isPlaceholder", 
                bg."categoryId", 
                (SELECT SUM(tn.amount) FROM transactions tn WHERE tn."userId"='{req.state.user}' AND EXTRACT(MONTH FROM tn.date) > 7 AND tn."categoryId" = bg."categoryId" AND tn.amount::text LIKE '%-%' ) AS spent, 
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
                AND t.row_num <=3
            WHERE 
                bg."userId" = '{req.state.user}'
            GROUP BY 
                bg."budgetId" """
        
        cursor.execute(sql)
        budgets = cursor.fetchall()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="database query error, try again")

    return {"success":True, "data":budgets}