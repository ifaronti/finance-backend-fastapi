from fastapi import Request
from ...utils.models import UpdateBudget
from ...pyscopg_connect import Connect
from psycopg2 import InterfaceError, OperationalError

def update_budget(data:UpdateBudget, req:Request):
    try:
        sql = f""" 
            UPDATE budget
            SET
                theme = COALESCE(%s, theme),
                maximum = COALESCE(%s, maximum),
                category = COALESCE(%s, category),
                categoryId = COALESCE(%s, "categoryId")
            WHERE budget."budgetId" = (%s)
            AND budget."userId" = '{req.state.user}'
        """
        params = (data.theme, data.maximum, data.category, data.categoryId, data.budgetId)
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
    return {"success":True, "message":"Budget updated successfully"}