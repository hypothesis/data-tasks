from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Timer:
    start_time: datetime = None
    """Time execution began."""

    duration: timedelta = None
    """Duration of query execution."""

    @contextmanager
    def time_it(self):
        self.start_time = datetime.now()

        yield

        self.duration = datetime.now() - self.start_time
