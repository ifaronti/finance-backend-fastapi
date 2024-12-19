from ...dependencies.password_manager import hash_password
from fastapi import Request
from ...utils.models import UserUpdate, GenericResponse
from ...pyscopg_connect import Connect
from psycopg2 import InterfaceError, OperationalError

def update_user(req:Request, details:UserUpdate)-> GenericResponse:
    if details.password:
        pass_hash = hash_password(details.password)
   
    sql = f""" UPDATE "user"
            SET 
                password = COALESCE(%s, password),
                email = COALESCE(%s, email),
                name = COALESCE(%s, name)
            WHERE id = %s
        """
    try:
        conn = Connect()
        dbconnect = conn.dbconnect()
        cursor = dbconnect.cursor()
        cursor.execute(sql, (pass_hash, details.email, details.name, req.state.user))
    except InterfaceError:
        raise InterfaceError
    except OperationalError as e:
        raise e
    except Exception:
        raise Exception
    finally:
        cursor.close()
        dbconnect.close()
    
    return {"success":True, "message":"User Account updated successfully"}


# COALESCE in the above sql query ensures that a non null value is used to update user.
# The 3 arguments for user_update are optional so a user can choose to update any of them meaning,
#pydantic won't throw any errors. so to ensure that a required field is not set to a null value,
#if the value is null in details, the value in the databse is unchaged hence email = COALESCE(%s, email) etc.