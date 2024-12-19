from .utils.config import Settings
import psycopg2 as sql
from psycopg2.extras import RealDictCursor
from psycopg2 import InterfaceError, OperationalError

settings = Settings()

class Connect:
    def __init__(self):
        pass

    def dbconnect(self):
        try:
            conn = sql.connect(
                dbname=settings.PGDATABASE,
                user=settings.PGUSER,
                host=settings.PGHOST,
                password=settings.PGPASSWORD,
                port=5432,
                cursor_factory=RealDictCursor
            )
            return conn
        
        except InterfaceError:
            conn =sql.connect(
                dbname=settings.PGDATABASE,
                user=settings.PGUSER,
                host=settings.PGHOST,
                password=settings.PGPASSWORD,
                port=5432,
                cursor_factory=RealDictCursor
            )
            print('Interface error occured. Reconnecting to database...')
            return conn
            
        except OperationalError:
            print('Operation error occured. Programmed not to reconnect. Please refresh')
            return None