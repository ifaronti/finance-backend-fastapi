from fastapi import HTTPException, status
from ...dependencies.password_manager import hash_password
from ...dependencies.placeholders import account_balance, placeholders
from ...utils.models import Register, GenericResponse
from psycopg2.extras import Json
from ...pyscopg_connect import Connect
from psycopg2 import InterfaceError, OperationalError
import uuid
from .auth_sqls import register_sql
user_id = str(uuid.uuid1())

def signup(user_details:Register)-> GenericResponse:
    queryDetails = dict(user_details).copy()
    hashed_pass = hash_password(user_details.password)
    balances = account_balance()
    acct_summary = account_balance()
    data = placeholders()
    queryDetails.update({
            "income":balances["income"], 
            "expenses":balances["expenses"],
            "balance":balances["balance"],
            "password":hashed_pass
    })
    try:
        conn = Connect()
        dbconnect = conn.dbconnect()
        cursor = dbconnect.cursor()
        
        cursor.execute(f""" SELECT id FROM "user" u WHERE email = '{queryDetails['email']}' """)
        user = cursor.fetchall()
        if user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')

        trns = Json(data["transactions"])
        bills = Json(data["bills"])
        budgets = Json(data["budgets"])
        pots = Json(data["pots"]) 

        params = (
            user_id,
            queryDetails['name'],
            queryDetails['email'],
            queryDetails['password'],
            acct_summary["income"],
            acct_summary["expenses"],
            acct_summary["balance"],
            trns, bills, budgets, pots
        )

        cursor.execute(register_sql, params)
        user = cursor.fetchone()
        dbconnect.commit()
    except InterfaceError:
        raise InterfaceError
    except OperationalError:
        raise OperationalError
    finally:
        cursor.close()
        dbconnect.close()

    return {"success":True, "message":"Account created"}
