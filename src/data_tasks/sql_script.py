import textwrap
from dataclasses import dataclass, field
from typing import List

import jinja2
import sqlparse

from data_tasks.sql_query import SQLQuery
from data_tasks.timer import Timer


@dataclass
class SQLScript:
    """A class representing an SQL file with multiple queries."""

    path: str
    """Full path of the script."""

    template_vars: dict
    """Template vars to pass to templated SQL statements."""

    queries: List[SQLQuery] = field(default_factory=list)
    """Queries contained in this file."""

    timing: Timer = field(default_factory=Timer)
    """Timer for query execution."""

    _jinja_env = jinja2.Environment(undefined=jinja2.StrictUndefined)

    def __post_init__(self):
        if not self.queries:
            self.queries = self._parse()

    def execute(self, connection, dry_run=False):
        """Execute this script with the given connection."""

        with self.timing.time_it():
            for query in self.queries:
                query.execute(connection, dry_run=dry_run)
                yield query

        yield self

    def dump(self, indent=""):
        """
        Get a string representation of this script.

        :param indent: Optional indenting string prepended to each line.
        """
        return textwrap.indent(
            f"SQL script: '{self.path}'\n"
            f"Executed {len(self.queries)} queries\n"
            f"Done in: {self.timing.duration}",
            indent,
        )

    def _parse(self):
        with open(self.path, encoding="utf-8") as handle:
            script_text = handle.read()

        if self.path.endswith("jinja2.sql"):
            # Looks like this file has been templated
            script_text = self._jinja_env.from_string(script_text).render(
                self.template_vars
            )

        return [
            SQLQuery(text=query, index=index)
            for index, query in (enumerate(sqlparse.split(script_text)))
            # Skip any empty queries
            if sqlparse.format(query, strip_comments=True).strip()
        ]
