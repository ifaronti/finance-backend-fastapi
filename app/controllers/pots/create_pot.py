from fastapi import status, HTTPException, Request
from ...utils.models import CreatePot
from ...pyscopg_connect import dbconnect

exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="An error occured; resource not created; check payload")

async def create_pot(data:CreatePot, req:Request):
    cursor = dbconnect.cursor()
    try:
        sql =f""" 
            INSERT INTO pots ("userId", name, target, total, theme)
            VALUES('{req.state.user}', %s, %s, %s, %s)
        """
        params = (data.name, data.target, data.total, data.theme)
        cursor.execute(sql, params)
        dbconnect.commit()
    except Exception:
        raise exception

    return {"success":True, "message": "Pot created successfully"}