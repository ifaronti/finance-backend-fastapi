from fastapi import Request, HTTPException, status
from ..pyscopg_connect import dbconnect
from .summary_sql import summary_query

def account_summary(req:Request):
    cursor = dbconnect.cursor()
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
        cursor.execute(summary_query, params)
        summary = cursor.fetchall()[0]
    
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="query error")
    return summary