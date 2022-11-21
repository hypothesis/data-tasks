from unittest.mock import create_autospec, sentinel

from data_tasks.sql_query import SQLQuery
from data_tasks.sql_script import SQLScript


class TestSQLScript:
    def test_dump(self):
        script = SQLScript(path="/long/path", template_vars={}, queries=[...])

        assert "/long/path" in script.dump()

    def test_execute(self):
        query = create_autospec(SQLQuery, spec_set=True, instance=True)
        script = SQLScript(path="/long/path", template_vars={}, queries=[query])

        items = list(script.execute(sentinel.connection, dry_run=sentinel.dry_run))

        assert items == [query, script]
        query.execute.assert_called_once_with(
            sentinel.connection, dry_run=sentinel.dry_run
        )
