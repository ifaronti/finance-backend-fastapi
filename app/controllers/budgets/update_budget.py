from fastapi import Request, HTTPException, status
from ...utils.models import UpdateBudget
from ...pyscopg_connect import dbconnect

def update_budget(data:UpdateBudget, req:Request):
    cursor = dbconnect.cursor()
    try:
        sql = f""" 
            UPDATE budget
            SET
                theme = COALESCE(%s, theme),
                maximum = COALESCE(%s, maximum),
                category = COALESCE(%s, category),
                categoryId = COALESCE(%s, "categoryId")
            WHERE budget."budgetId" = (%s)
            AND budget."userId" = '{req.state.user}'
        """
        params = (data.theme, data.maximum, data.category, data.categoryId, data.budgetId)
        cursor.execute(sql, params)
        dbconnect.commit()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Budget not updated try again")

    return {"success":True, "message":"Budget updated successfully"}