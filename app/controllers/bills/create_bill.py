from fastapi import Request
from ...utils.models import CreateBill, GenericResponse
from ...pyscopg_connect import Connect
from psycopg2 import InterfaceError, OperationalError

def create_bill(data:CreateBill, req:Request)->GenericResponse:
    sql = f"""
        INSERT INTO bills ("userId", amount, name, avatar, category, "categoryId", due_day)
        VALUES('{req.state.user}', %s, %s, %s, %s, %s, %s)
    """
    params = (
        data.amount,
        data.name,
        data.avatar,
        data.category,
        data.categoryId,
        data.due_day
    )

    try:
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

    return {"success":True, "message":"Bill successfully added to account"}