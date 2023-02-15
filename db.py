import psycopg2

from config import settings


def get_pg_db():
    db_url = settings.SQLALCHEMY_DATABASE_URI
    print("db_url: ", db_url)
    return db_url


job_service_db = psycopg2.connect(
    get_pg_db()
)
