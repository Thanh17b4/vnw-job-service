import glob
from unittest import TestCase

import psycopg2
from fastapi.testclient import TestClient

from config import settings
from main import app


class EngineTestCase(TestCase):
    client = TestClient(app)

    @staticmethod
    def setup_database():
        # Create the test tables
        conn = psycopg2.connect(settings.SQLALCHEMY_TEST_DATABASE_URI)
        cur = conn.cursor()
        file_create_and_insert_job_records = glob.glob('../migration/*.job.up.sql')
        for file_create_and_insert_job_record in file_create_and_insert_job_records:
            with open(file_create_and_insert_job_record) as f:
                query = f.read()
                cur.execute(query)

        files = glob.glob('../migration/*.job_category.up.sql')
        files.sort()
        for i in range(len(files)):
            with open(files[i], 'r') as f:
                sql = f.read()
                cur.execute(sql)
                conn.commit()
        cur.close()

    @staticmethod
    def teardown_database():
        # Drop the test tables
        conn = psycopg2.connect(settings.SQLALCHEMY_TEST_DATABASE_URI)
        cur = conn.cursor()
        files = glob.glob('../migration/*.job_category.down.sql')
        files.sort()
        for file in files:
            with open(file, 'r') as f:
                sql = f.read()
                cur.execute(sql)
        cur.execute('DROP TABLE jobs')
        conn.commit()
        cur.close()
