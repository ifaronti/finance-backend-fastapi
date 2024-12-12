from fastapi import HTTPException, Request, status
from typing import Optional
from ...pyscopg_connect import dbconnect
from datetime import datetime
from ...utils.sort_transacions import sort_transactions

prisma_exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="An error occured")

async def get_bills(req:Request, 
                    skip:Optional[int]=0, 
                    name:Optional[str]=None, 
                    sort:Optional[str]="Latest"
                ):
    
    item_sort = sort_transactions(sort, createdAt=True)
    today = datetime.now().day
    cursor = dbconnect.cursor()

    try:
        sql = f"""
            WITH bill_day AS(
                SELECT
                    b.name,
                    b.amount,
                    b.due_day,
                    b.avatar,
                    b."userId",
                    CASE
                        WHEN (b.due_day <= {today}) THEN 'paid'
                        WHEN (b.due_day > {today}) AND (b.due_day - {today} < 7) THEN 'soon'
                        WHEN (31 - {today} <= 4) AND (b.due_day < 4) THEN 'soon'
                        ELSE 'upcoming'
                    END AS status,
                    ROW_NUMBER() OVER (PARTITION BY b."billId" ORDER BY {item_sort}) AS b_row
                FROM bills b
            )
            SELECT json_agg(bill_day) as bills FROM bill_day
            WHERE bill_day."userId" = '{req.state.user}'
            {f'AND position({name} IN LOWER(bill_day.name))>0' if name else ''}
            AND bill_day.b_row <= 10
            OFFSET {skip}
        """
        cursor.execute(sql)
        bills = cursor.fetchall()
    except:
        raise prisma_exception
    
    bills_copy = list(bills)

    if len(bills_copy) < 10:
        isLastPage = True
    else:
        isLastPage = False
    
    return {"success":True, "data":bills_copy[0], "isLastPage":isLastPage}