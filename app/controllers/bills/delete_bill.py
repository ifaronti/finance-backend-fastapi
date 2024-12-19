from fastapi import HTTPException, Request, status
from ...pyscopg_connect import Connect
from psycopg2 import InterfaceError, OperationalError

def delete_bill(id:int, req:Request):
    sql = f"""
        DELETE FROM bills
        WHERE "billId" = %s
        AND "userId" = %s
    """
    try:
        conn = Connect()
        dbconnect = conn.dbconnect()
        cursor = dbconnect.cursor()
        cursor.execute(sql, (id, req.state.user))
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

    return {"success":True, "message":"Bill deleted successfully"}