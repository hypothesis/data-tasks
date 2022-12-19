import os

import pytest
import sqlalchemy

TEST_SETTINGS = {
    "database_url": os.environ["TEST_DATABASE_URL"],
}


@pytest.fixture(scope="session")
def db_engine():
    db_engine = sqlalchemy.create_engine(TEST_SETTINGS["database_url"])
    yield db_engine

    db_engine.dispose()
