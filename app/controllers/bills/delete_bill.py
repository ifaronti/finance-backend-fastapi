from fastapi import HTTPException, Request, status
from ...pyscopg_connect import dbconnect

prisma_exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="An error occured")

def delete_bill(id:int, req:Request):
    sql = f"""
        DELETE FROM bills
        WHERE "billId" = %s
        AND "userId" = %s
    """
    cursor = dbconnect.cursor()
    try:
        cursor.execute(sql, (id, req.state.user))
        dbconnect.commit()
    except Exception:
        raise prisma_exception

    return {"success":True, "message":"Bill deleted successfully"}