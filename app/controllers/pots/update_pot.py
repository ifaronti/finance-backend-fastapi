from fastapi import Request, status, HTTPException
from ...utils.models import UpdatePot, GenericResponse
from typing import Optional
from ...pyscopg_connect import dbconnect

exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="An error occured")

def update_pot(req:Request, 
               data:UpdatePot, 
               add:Optional[int]=None, 
               subtract:Optional[int]=None
            )->GenericResponse:
    cursor = dbconnect.cursor()
    try:
        sql = f"""
            WITH pot_update AS(
                UPDATE pots
                    SET
                        name = COALESCE(%s, name),
                        theme = COALESCE(%s, theme),
                        total= COALESCE(total + %s, total - %s, total),
                        target = COALESCE(%s, target)
                WHERE "potId" = %s
                AND "userId" = '{req.state.user}'
            )
            UPDATE "user"
                SET
                    balance = COALESCE(balance + %s, balance - %s, balance)
            WHERE id = '{req.state.user}'
        """

        params = (
            data.name,
            data.theme,
            subtract,
            add,
            data.target if not 0 else None,
            data.potId if not 0 else None,
            add,
            subtract
        )

        cursor.execute(sql, params)
        dbconnect.commit()
    except:
        raise exception
    
    return {"success":True, "message":"Pot updated successfully."}