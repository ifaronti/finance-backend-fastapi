from ...utils.models import CreateBudget
from fastapi import Request, HTTPException, status
from ...pyscopg_connect import dbconnect

async def create_budget(data:CreateBudget, req:Request):
    cursor = dbconnect.cursor()
    try:
        sql = f"""
            INSERT INTO budgets ("userId", maximum, theme, "categoryId", category)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (req.state.user, data.maximum, data.theme, data.categoryId, data.category)
        cursor.execute(sql, params)
        dbconnect.commit()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error occured")
        
    return {"success":True, "message": "Budget created successfully"}