from fastapi.testclient import TestClient
from app.main import app

from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from app.database import get_db, Base
from faker import Faker
# SETUP TESTS TO USE A SEPERATE DB INSTEAD OF THE ONE USED FOR DEVELOPMENT
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False , autoflush=False, bind=engine)

# CREATE DB TABLES ON TEST DB BEFORE TESTING 
def create_db_tables():
    Base.metadata.create_all(bind=engine)
def drop_db_tables():
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
# This fixture creates all the db tables before running the tests 
# and drops the DB tables after running tests
def session():
    """ This fixture creates all the db tables and the database session """
    # run our code and drop any existing tables before the tests
    drop_db_tables()
    # run our code to create tables for the tests
    create_db_tables()
    # yield delays the test
    # create the db session here 
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    print("my session fixture ran")
    """ This fixture is dependent on the session fixture and is used to create a test client that is dependent on the session.
        It runs a session for each test done and this makes it possile to use the client or 
        query the DB object directly using the session e.g => (session.query(Model).filter(Model.id == "email"))."""
    def override_get_db():
        try: 
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    


