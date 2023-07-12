import pytest
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from tests.factories.factoryboy_sqlalchemy_session import (
    clear_factoryboy_sqlalchemy_session,
    set_factoryboy_sqlalchemy_session,
)


@pytest.fixture
def db_session(db_engine):
    """
    Yield the SQLAlchemy session object.

    We enable fast repeatable database tests by setting up the database only
    once per session (see :func:`db_engine`) and then wrapping each test
    function in a transaction that is rolled back.

    Additionally, we set a SAVEPOINT before entering the test, and if we
    detect that the test has committed (i.e. released the savepoint) we
    immediately open another. This has the effect of preventing test code from
    committing the outer transaction.

    """
    conn = db_engine.connect()
    trans = conn.begin()
    session = sessionmaker()(bind=conn)
    session.begin_nested()
    set_factoryboy_sqlalchemy_session(session)

    @sqlalchemy.event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        if (
            transaction.nested
            and not transaction._parent.nested  # pylint: disable=protected-access
        ):
            session.begin_nested()

    try:
        yield session
    finally:
        clear_factoryboy_sqlalchemy_session()
        session.close()
        trans.rollback()
        conn.close()
