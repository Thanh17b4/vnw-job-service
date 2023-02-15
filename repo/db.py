import psycopg2


def connect(dns: str):
    pgsql_db = psycopg2.connect(dns)
    return pgsql_db
