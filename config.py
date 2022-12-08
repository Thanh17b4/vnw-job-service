import psycopg2

mydb = psycopg2.connect(
    host="localhost",
    database="jobs_service",
    user="thanhpv",
    password="22121992"
)
