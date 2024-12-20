from fastapi import HTTPException, status, Request
from ...pyscopg_connect import Connect
from psycopg2 import InterfaceError, OperationalError

def delete_budget(id:int, req:Request):
    try:
        sql = f"""
            DELETE FROM budgets
            WHERE "budgetId" = %s
            AND budgets."userId" = '{req.state.user}'
        """
        conn = Connect()
        dbconnect = conn.dbconnect()
        cursor = dbconnect.cursor()
        cursor.execute(sql, (id,))  #the comma is necessary so it's read as a turple else it will throw error.
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
    return {"success":True, "message":"Budget deleted successfully"}