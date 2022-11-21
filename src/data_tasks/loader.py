import os
import os.path

from data_tasks.python_script import PythonScript
from data_tasks.sql_script import SQLScript


def from_dir(task_dir: str, template_vars: dict):
    """
    Generate script objects from files found in a directory.

    This will return a generator of script objects based on the natural sorting
    order of files found in the directory, and subdirectories. Only files
    with a `.sql` or `.py` prefix are considered. Files with `.jinja2.sql` are
    treated as Jinja2 templated SQL and are rendered using the provided
    environment.

    :param task_dir: The directory to read from
    :param template_vars: Variables to include in Jinja2 SQL files

    :raises NotADirectoryError: if `task_dir` is not a directory
    """
    if not os.path.isdir(task_dir):
        raise NotADirectoryError(f"Cannot find the task directory: '{task_dir}'")

    for item in sorted(os.listdir(task_dir)):
        full_name = os.path.join(task_dir, item)

        if os.path.isdir(full_name):
            yield from from_dir(full_name, template_vars=template_vars)

        elif full_name.endswith(".sql"):
            yield SQLScript(full_name, template_vars=template_vars)

        elif full_name.endswith(".py"):
            yield PythonScript(full_name)
