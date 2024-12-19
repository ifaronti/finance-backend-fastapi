from fastapi import Request
from ...utils.models import CreatePot
from ...pyscopg_connect import Connect
from psycopg2 import InterfaceError, OperationalError

def create_pot(data:CreatePot, req:Request):
    try:
        sql =f""" 
            INSERT INTO pots ("userId", name, target, total, theme)
            VALUES('{req.state.user}', %s, %s, %s, %s)
        """
        params = (data.name, data.target, data.total, data.theme)
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

    return {"success":True, "message": "Pot created successfully"}