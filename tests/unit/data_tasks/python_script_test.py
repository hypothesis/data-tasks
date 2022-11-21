from unittest.mock import sentinel

import pytest
from importlib_resources import files

from data_tasks.python_script import PythonScript


class TestPythonScript:
    def test_it(self, python_script):
        assert python_script.module
        assert python_script.result is None

    def test_parsing_a_script_without_main(self, empty_script):
        with pytest.raises(ModuleNotFoundError):
            PythonScript(path=empty_script)

    def test_dump(self):
        script = PythonScript(path="/long/path/some_script.py", module=...)

        assert "/long/path/some_script.py" in script.dump()

    def test_execute(self, python_script):
        items = list(python_script.execute(sentinel.connection))

        assert items == [python_script]
        assert python_script.result == "script_run"

    def test_execute_with_dry_run(self, python_script):
        items = list(python_script.execute(sentinel.connection, dry_run=True))

        assert items == [python_script]
        assert python_script.result is None

    @pytest.fixture
    def empty_script(self, tmp_path):
        empty_script = tmp_path / "script.py"
        empty_script.write_text("")

        return empty_script

    @pytest.fixture
    def python_script(self):
        fixture_dir = files("tests.unit.data_tasks") / "script_fixture"

        return PythonScript(path=str(fixture_dir / "04_file.py"))
