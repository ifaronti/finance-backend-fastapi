from fastapi import status, HTTPException, Request
from ...pyscopg_connect import dbconnect

exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="An error occured check id params")


def delete_pot(id:int, req:Request):
    cursor = dbconnect.cursor()
    try:
        sql = f""" 
            DELETE FROM pots
            WHERE "potId" = %s
            AND "userId" = '{req.state.user}'
        """
        cursor.execute(sql, (id,))
        dbconnect.commit()
    except:
        raise exception

    return {"success":True, "message":"Pot deleted"}