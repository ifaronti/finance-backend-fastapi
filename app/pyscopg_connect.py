from .utils.config import Settings
import psycopg2 as sql
from psycopg2.extras import RealDictCursor

settings = Settings()

dbconnect = sql.connect(
    dbname=settings.PGDATABASE,
    user=settings.PGUSER,
    host=settings.PGHOST,
    password=settings.PGPASSWORD,
    port=5432,
    cursor_factory=RealDictCursor
)

cursor = dbconnect.cursor(cursor_factory=RealDictCursor)

