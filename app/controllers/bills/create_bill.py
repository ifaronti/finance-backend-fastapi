from fastapi import Request
from ...utils.models import CreateBill, GenericResponse
from ...pyscopg_connect import dbconnect

def create_bill(data:CreateBill, req:Request)->GenericResponse:
    sql = f"""
        INSERT INTO bills ("userId", amount, name, avatar, category, categoryId, due_day)
        VALUES('{req.state.user}', %s, $s, $s, $s, $s, $s)
    """
    params = (
        data.amount,
        data.name,
        data.avatar,
        data.category,
        data.categoryId,
        data.due_day
    )
    
    cursor = dbconnect.cursor()

    try:
        cursor.execute(sql, params)
        dbconnect.commit()
    except Exception as e:
        raise e.message

    return {"success":True, "message":"Bill successfully added to account"}