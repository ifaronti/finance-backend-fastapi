from ...utils.models import CreateBudget
from fastapi import Request
from ...pyscopg_connect import Connect
from psycopg2 import InterfaceError, OperationalError

def create_budget(data:CreateBudget, req:Request):
    cursor = dbconnect.cursor()
    try:
        sql = f"""
            INSERT INTO budgets ("userId", maximum, theme, "categoryId", category)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (req.state.user, data.maximum, data.theme, data.categoryId, data.category)
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
    return {"success":True, "message": "Budget created successfully"}