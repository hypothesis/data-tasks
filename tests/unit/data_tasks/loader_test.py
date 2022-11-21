import pytest
from h_matchers import Any
from importlib_resources import files

from data_tasks.loader import from_dir
from data_tasks.python_script import PythonScript
from data_tasks.sql_query import SQLQuery
from data_tasks.sql_script import SQLScript


class TestTask:
    def test_from_dir(self):
        fixture_dir = files("tests.unit.data_tasks") / "script_fixture"

        template_vars = {"template_var": "template_value"}

        scripts = list(from_dir(task_dir=str(fixture_dir), template_vars=template_vars))

        assert scripts == [
            SQLScript(
                path=str(fixture_dir / "01_file.sql"),
                template_vars=template_vars,
                queries=[
                    SQLQuery(index=0, text="-- Comment 1\nSELECT 1;"),
                    SQLQuery(index=1, text="-- Comment 2\nSELECT 2;"),
                ],
            ),
            SQLScript(
                path=str(fixture_dir / "02_dir/01_file.sql"),
                template_vars=template_vars,
                queries=[SQLQuery(index=0, text="SELECT 3")],
            ),
            SQLScript(
                path=str(fixture_dir / "03_file.jinja2.sql"),
                template_vars=template_vars,
                queries=[SQLQuery(index=0, text="SELECT 'template_value';")],
            ),
            PythonScript(path=str(fixture_dir / "04_file.py"), module=Any()),
            SQLScript(
                path=str(fixture_dir / "05_empty.sql"),
                template_vars=template_vars,
                queries=[],
            ),
            SQLScript(
                path=str(fixture_dir / "06_trailing_comment.sql"),
                template_vars=template_vars,
                queries=[SQLQuery(index=0, text="-- Comment\nSELECT 1;")],
            ),
        ]

    def test_from_dir_raises_for_missing_dir(self):
        with pytest.raises(NotADirectoryError):
            list(from_dir("/i_do_not_exist", {}))
