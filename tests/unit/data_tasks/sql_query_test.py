from pytest import fixture

from data_tasks.sql_query import SQLQuery


class TestSQLQuery:
    def test_execute(self, query, connection):
        self.assert_query_null_pre_execute(query)

        query.execute(connection)

        assert query.rows == [("value",)]
        assert query.columns == ["column"]
        assert query.timing.start_time is not None

    def test_execute_with_params(self, connection):
        query = SQLQuery(0, "SELECT :value")

        query.execute(connection, parameters={"value": 12})

        assert query.rows == [(12,)]

    def test_execute_with_dry_run(self, connection):
        query = SQLQuery(0, "THIS IS NOT SQL")
        self.assert_query_null_pre_execute(query)

        query.execute(connection, dry_run=True)

        assert query.timing.start_time is not None

    def test_execute_with_a_query_returning_no_rows(self, query_no_rows, connection):
        self.assert_query_null_pre_execute(query_no_rows)

        query_no_rows.execute(connection)

        assert query_no_rows.rows is None
        assert query_no_rows.columns is None
        assert query_no_rows.timing.start_time is not None

    def test_dump(self, query, connection):
        query.execute(connection)

        text = query.dump(indent=">>> ")
        # We're not going to assert everything about this. The exact formatting
        # doesn't matter. So this is more of a smoke test to show it's not
        # totally broken
        assert text.startswith(
            """>>> 0=> SELECT 'value' AS column
>>> +----------+
>>> | column   |
>>> |----------|
>>> | value    |
>>> +----------+"""
        )

    def test_dump_cleans_secrets(self, query_with_secret):
        assert query_with_secret.dump().startswith(
            """0=> SELECT
0=>             ********** ** **** ** ******
0=>             'value' AS column"""
        )

    def test_dump_works_with_no_rows(self, query_no_rows):
        assert query_no_rows.dump()

    def assert_query_null_pre_execute(self, query):
        assert query.rows is None
        assert query.columns is None
        assert query.timing.start_time is None

    @fixture
    def connection(self, db_session):
        return db_session.bind

    @fixture
    def query(self):
        return SQLQuery(0, "SELECT 'value' AS column")

    @fixture
    def query_no_rows(self):
        return SQLQuery(0, "ANALYZE")

    @fixture
    def query_with_secret(self):
        return SQLQuery(
            0,
            """SELECT
            'password` AS pass -- secret
            'value' AS column""",
        )
