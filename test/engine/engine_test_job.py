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
        files = glob.glob('../migration/*.job.up.sql')
        for file in files:
            with open(file, 'r') as f:
                sql = f.read()
                cur.execute(sql)
                conn.commit()
        cur.close()

    @staticmethod
    def teardown_database():
        # Drop the test tables
        conn = psycopg2.connect(settings.SQLALCHEMY_TEST_DATABASE_URI)
        cur = conn.cursor()
        files = glob.glob('../migration/*.job.down.sql')
        for file in files:
            with open(file, 'r') as f:
                sql = f.read()
                cur.execute(sql)
        conn.commit()
        cur.close()
