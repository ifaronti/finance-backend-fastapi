from fastapi import Request, status, HTTPException
from typing import Optional
from ...pyscopg_connect import dbconnect
from ...utils.models import GenericResponse

exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="An error occured check id params")

def get_pots(req:Request, skip:Optional[int]=0)->GenericResponse:
    cursor = dbconnect.cursor()
    try:
        sql = f""" 
            SELECT p.target, p.theme, p.name, p.total, p."potId"
            FROM pots p
            WHERE "userId" = '{req.state.user}'
            ORDER BY p.name DESC
            OFFSET %s
        """
        cursor.execute(sql, (skip,))
        pots = cursor.fetchall()
    except:
        raise exception

    return {"success":True, "data":pots}