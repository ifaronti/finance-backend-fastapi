from fastapi import Request
from ...pyscopg_connect import Connect
from psycopg2 import InterfaceError, OperationalError

def delete_pot(id:int, req:Request):
    try:
        sql = f""" 
            DELETE FROM pots
            WHERE "potId" = %s
            AND "userId" = '{req.state.user}'
        """
        conn = Connect()
        dbconnect = conn.dbconnect()
        cursor = dbconnect.cursor()
        cursor.execute(sql, (id,))
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

    return {"success":True, "message":"Pot deleted"}