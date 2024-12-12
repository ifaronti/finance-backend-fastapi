from fastapi import status, HTTPException, Request
from ...utils.sort_transacions import sort_transactions
from ...pyscopg_connect import dbconnect
from typing import Optional

def get_Transactions(req:Request,
                        sort:str, 
                        category:str,  
                        skip:Optional[int]=0, 
                        name:Optional[str]= None
                    ):
    items_sort = sort_transactions(sort)
    cursor = dbconnect.cursor()
    if category == "All":
        category = None
    try:
        sql = f""" 
            SELECT * FROM transactions t 
            WHERE t."userId" = '{req.state.user}'
            {f"AND position('{category.strip("'Category.'")}' IN t.category)>0" if category else ''}
            {f" {f"AND position(LOWER('{name}') IN LOWER(t.name))>0" if name else ''} "}
            ORDER BY {items_sort}
            OFFSET %s
            LIMIT 10
        """
        params = (skip,)
        cursor.execute(sql, params)
        transactions = cursor.fetchall()

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Query Error')

    if len(transactions) <10:
        isLastPage = True
    else:
        isLastPage = False

    return {"success":True, "data":{"transactions":transactions, "isLastPage":isLastPage}}