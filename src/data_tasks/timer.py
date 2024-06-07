from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Union


@dataclass
class Timer:
    start_time: Union[datetime, None] = None
    """Time execution began."""

    duration: Union[timedelta, None] = None
    """Duration of query execution."""

    @contextmanager
    def time_it(self):
        self.start_time = datetime.now()

        yield

        self.duration = datetime.now() - self.start_time
