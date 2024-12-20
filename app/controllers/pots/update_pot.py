from fastapi import Request
from ...utils.models import UpdatePot, GenericResponse
from typing import Optional
from ...pyscopg_connect import Connect
from psycopg2 import InterfaceError, OperationalError

def update_pot(req:Request, 
               data:UpdatePot, 
               add:Optional[int]=None, 
               subtract:Optional[int]=None
            )->GenericResponse:
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
            subtract,
            add
        )
        conn = Connect()
        dbconnect = conn.dbconnect()
        cursor = dbconnect.cursor()
        cursor.execute(sql, params)
        dbconnect.commit()
    except InterfaceError as i:
        raise i
    except OperationalError as o:
        raise o
    except Exception as e:
        raise e
    finally:
        cursor.close()
        dbconnect.close()
    
    return {"success":True, "message":"Pot updated successfully."}