from fastapi import HTTPException, status
from ...dependencies.token import create_token
from ...dependencies.password_manager import verify_password
from ...utils.models import Login
from ...pyscopg_connect import dbconnect
from typing import Dict

not_found = HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="User not found")

invalid_credentials = HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                    detail="Invalid credentials")

def logon(auth_details:Login)->Dict:
    sql = f""" SELECT
                    u.name,
                    u.id,
                    u.password
                FROM "user" u 
                WHERE u.email = '{auth_details.username}'
            """
    cursor = dbconnect.cursor()
    cursor.execute(sql)
    user = cursor.fetchone()
    # # cursor.close()
    # dbconnect.close()

    if not user:
        raise not_found
    
    isMatch = verify_password(auth_details.password, user["password"])

    if not isMatch:
        raise invalid_credentials

    token = create_token(user["id"])
    return {"name":user["name"], "access_token":token, "success":True, "token_type":"Bearer"}
