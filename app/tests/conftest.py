import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database

from app.api.dependency import get_db
from app.core.config import settings
from app.db.base_class import Base
from app.main import app
SQLALCHEMY_DATABASE_URL = settings.TEST_DATABASE_URL


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    if not database_exists:
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()

    # begin a non-ORM transaction
    connection.begin()

    # bind an individual Session to the connection
    db = Session(bind=connection)
    # db = Session(db_engine)

    # `dependency_overrides` is a dictionary that maps dependencies to their replacement func.
    # lambda wil return our Session instead of creating a new Session.
    app.dependency_overrides[get_db] = lambda: db

    yield db

    db.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):

    # Even though fixture has a param `db`, we still use `lambda` func to return db.
    # Because the `lambda` function ensures that the correct `db` obj is passed.
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c




