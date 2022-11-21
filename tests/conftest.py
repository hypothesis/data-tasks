import os

import pytest
import sqlalchemy

TEST_SETTINGS = {"database_url": os.environ.get("TEST_DATABASE_URL", "sqlite://")}


@pytest.fixture(scope="session")
def db_engine():
    db_engine = sqlalchemy.create_engine(TEST_SETTINGS["database_url"])
    yield db_engine

    db_engine.dispose()
