from fastapi import Request, status, HTTPException
from typing import Optional
from ...pyscopg_connect import Connect
from psycopg2 import InterfaceError, OperationalError
from ...utils.models import GenericResponse

exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="An error occured check id params")

def get_pots(req:Request, skip:Optional[int]=0)->GenericResponse:
    try:
        sql = f""" 
            SELECT p.target, p.theme, p.name, p.total, p."potId"
            FROM pots p
            WHERE "userId" = '{req.state.user}'
            ORDER BY p.name DESC
            OFFSET %s
        """
        conn = Connect()
        dbconnect = conn.dbconnect()
        cursor = dbconnect.cursor()
        cursor.execute(sql, (skip,))
        pots = cursor.fetchall()
    except InterfaceError as i:
        raise i
    except OperationalError as o:
        raise o
    except Exception as e:
        raise e
    finally:
        cursor.close()
        dbconnect.close()

    return {"success":True, "data":pots}