import textwrap
from dataclasses import dataclass, field
from importlib.util import module_from_spec, spec_from_file_location
from types import ModuleType
from typing import Any, Optional

from data_tasks.timer import Timer


@dataclass
class PythonScript:
    """A class representing a Python script.

    This requires you to define a Python file with a `main(**kwargs)` function
    which will be passed the connection object.
    """

    path: str
    """Full path of the script."""

    timing: Timer = field(default_factory=Timer)
    """Timer for query execution."""

    module: ModuleType = None
    """The module loaded from the script."""

    result: Optional[Any] = None
    """The result of executing `main()` if any."""

    def __post_init__(self):
        if self.module:
            return

        # Generate a "spec" for the module
        spec = spec_from_file_location(f"script_{id(self)}", self.path)

        # Create a module from the spec
        self.module = module_from_spec(spec)

        # Trigger processing of the module
        spec.loader.exec_module(self.module)

        if not hasattr(self.module, "main"):
            raise ModuleNotFoundError(
                f"Expected to find `main()` function in {self.path}"
            )

    def execute(self, connection, dry_run=False):
        """Execute the python script."""

        with self.timing.time_it():
            # pylint: disable=no-member
            if not dry_run:
                self.result = self.module.main(connection=connection)

        yield self

    def dump(self, indent=""):
        """
        Get a string representation of this script.

        :param indent: Optional indenting string prepended to each line.
        """

        return textwrap.indent(
            f"Python script: '{self.path}'\nDone in: {self.timing.duration}", indent
        )
