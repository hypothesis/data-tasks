from datetime import datetime, timedelta

from h_matchers import Any

from data_tasks.timer import Timer


class TestTimer:
    def test_it(self):
        timer = Timer()
        assert timer.start_time is None
        assert timer.duration is None

        with timer.time_it():
            pass

        assert timer.start_time == Any.instance_of(datetime)
        assert (timer.start_time - datetime.now()) < timedelta(seconds=1)
        assert timer.duration == Any.instance_of(timedelta)
        assert timer.duration <= timedelta(seconds=1)
