from fastapi import HTTPException, status, Request
from ...pyscopg_connect import dbconnect

def delete_budget(id:int, req:Request):
    cursor = dbconnect.cursor()
    try:
        sql = f"""
            DELETE FROM budgets
            WHERE "budgetId" = %s
            AND budgets."userId = '{req.state.user}'
        """
        cursor.execute(sql, (id,))  #the comma is necessary so it's read as a turple else it will throw error.
        dbconnect.commit()

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Budget is not deleted, try again")

    return {"success":True, "message":"Budget deleted successfully"}