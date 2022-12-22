from unittest import TestCase

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base, create_session

from config import settings
from main import app

engine = create_engine(settings.SQLALCHEMY_TEST_DATABASE_URI)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def override_create_session():  # Each time, a session is being generated, they will execute, then close..... then generate a new one -> repeat
    db = session_local()
    try:
        yield db
    finally:
        db.close()


class EngineTestCase(TestCase):
    meta = MetaData()
    client = TestClient(app)
    app.dependency_overrides[create_session] = override_create_session
    _token = None

    # setUp some record for the test
    def setUp(self):
        # Setting a new database and connects
        Base.metadata.drop_all(bind=engine)
        # Base.metadata.create_all(engine)
        # with engine.connect() as con:
        #     filename = os.path.join(
        #         Path(__file__).parent, "../migration", "20221125.00.insert_record.sql"
        #     )
        #     with open(filename) as file:
        #         query = text(file.read())
        #         con.execute(query)

    # tearDown func to auto clean all the record after test
    def tearDown(self):
        Base.metadata.drop_all(engine)
        self.client.close()
        ...
