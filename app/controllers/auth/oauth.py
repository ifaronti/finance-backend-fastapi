from ...dependencies.githubprovider import get_user
from ...dependencies.token import create_token
from ...utils.models import LoginResponse
from ...pyscopg_connect import Connect
from psycopg2 import InterfaceError, OperationalError
from ...dependencies.placeholders import account_balance, placeholders
from psycopg2.extras import Json
import uuid
from .auth_sqls import register_sql

def github_login(code:str) -> LoginResponse:
    auth_data = get_user(code)
    acct_summary = account_balance()
    data = placeholders()
    user_id = str(uuid.uuid1())
    conn = Connect()
    dbconnect = conn.dbconnect()
    cursor = dbconnect.cursor()

    cursor.execute(f""" SELECT githubid FROM "user" u WHERE u.email = '{auth_data['email']}' """)
    user = cursor.fetchone()

    if not user:
        params = (
                user_id,
                auth_data['name'], 
                auth_data['email'],
                auth_data['avatar_url'],
                auth_data['id'],
                acct_summary["income"],
                acct_summary["expenses"],
                acct_summary["balance"],
                trns, bills, budgets, pots
        )

        trns = Json(data["transactions"])
        bills = Json(data["bills"])
        budgets = Json(data["budgets"])
        pots = Json(data["pots"])

        try:
            conn = Connect()
            dbconnect = conn.dbconnect()
            cursor = dbconnect.cursor()
            cursor.execute(register_sql, params)
            dbconnect.commit()
            user = cursor.fetchone()
        except InterfaceError:
            raise InterfaceError
        except OperationalError:
            raise OperationalError
        except Exception:
            raise Exception
        finally:
            cursor.close()
            dbconnect.close()
        
    token = create_token(user[0]["id"])

    return {"name":user["name"], "success":True, "access_Token":token, "token_type":"Bearer"}

# # Use execute_values to efficiently insert multiple rows
# execute_values(cur, insert_query, [(value,) for value in values])

#or like I have above