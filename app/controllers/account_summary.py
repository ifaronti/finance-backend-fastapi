from fastapi import Request
from ..pyscopg_connect import Connect
from psycopg2 import InterfaceError, OperationalError
from .summary_sql import summary_query

def account_summary(req:Request):
    try:
        params = (
            req.state.user,
            req.state.user,
            req.state.user,
            req.state.user,
            req.state.user,
            req.state.user,
            req.state.user,
            req.state.user,
        )
        conn = Connect()
        dbconnect = conn.dbconnect()
        cursor = dbconnect.cursor()
        cursor.execute(summary_query, params)
        summary = cursor.fetchall()[0]
    
    except InterfaceError as i:
        raise i
    except OperationalError as o:
        raise o
    except Exception as e:
        raise e
    finally:
        cursor.close()
        dbconnect.close()
    return summary