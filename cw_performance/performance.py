# coding=utf-8
__author__ = 'Cezary Wagner'
__copyright__ = 'Copyright 2015-2019, Cezary K. Wagner.'
__license__ = 'Apache License 2.0'
__version__ = '1.0'

import datetime
import time


class Speedometer(object):
    """
    Measure speed of events = events/seconds.

    Speedometer works like that:
    __init__()
    start()
    add_event()
    get_speed() -> now speed
    stop()
    get_speed() -> stop speed

    You can start it again and again:
    start()
    add_event()
    get_speed() -> previous + now speed
    stop()
    get_speed() -> previous + stop speed

    Or reset:
    reset()

    """

    def __init__(self):
        self.start_time = None
        self.stop_time = None
        self.events = None
        self.seconds = None

    def start(self, start_time=None):
        """
        Start speed measuring.
        :param: start_time: Start time if None it is now.
        """

        if self.start_time is not None:
            raise RuntimeError('Speedometer is already started.')

        if start_time:
            self.start_time = start_time
        else:
            self.start_time = time.perf_counter()
        self.stop_time = None
        if self.events is None or self.seconds is None:
            self.events = 0
            self.seconds = 0.0

    def add_event(self):
        """ Add event. """

        if not self.start_time:
            raise RuntimeError('Speedometer is not started.')
        self.events += 1

    def add_events(self, events):
        """ Add events. """

        if not self.start_time:
            raise RuntimeError('Speedometer is not started.')
        self.events += events

    def get_events(self):
        """
        Get total events counter since last reset.
        :return: Events counter or None if it has never started.
        """

        return self.events

    def get_seconds(self):
        """
        Get total seconds counter since last reset.
        :return: Seconds counter or None if it has never started.
        """

        # get total + current speed
        if self.start_time:
            now = time.perf_counter()
            seconds = now - self.start_time
            # add previous seconds
            seconds += self.seconds
            return seconds
        # get total speed
        else:
            return self.seconds

    def get_speed(self):
        """
        Get speed of events/seconds using now time or stop time since last reset.
        :return: speed or None if zero seconds
        """

        seconds = self.get_seconds()
        return self.events / seconds if seconds else None

    def stop(self, stop_time=None):
        """
        Stop speed measuring.
        :param stop_time: Stop time if None it is now.
        """

        if self.start_time is None:
            raise RuntimeError('Speedometer is not started.')

        if stop_time:
            self.stop_time = stop_time
        else:
            self.stop_time = time.perf_counter()
        seconds = self.stop_time - self.start_time
        # add previous seconds
        self.seconds += seconds
        # reset times
        self.start_time = None
        self.stop_time = None


class ProgressMeter(object):
    """
    Measure speed of events = events/seconds.

    Progress meter works like that:
    __init__()
    start()
    add_event()
    get_speed() -> now speed
    stop()
    get_speed() -> stop speed

    You can start it again and again:
    start()
    add_event()
    get_speed() -> previous + now speed
    stop()
    get_speed() -> previous + stop speed

    """

    def __init__(self, total_events):
        self.total_events = total_events
        self.start_time = None
        self.stop_time = None
        self.events = None
        self.seconds = None

    def start(self, start_time=None):
        """
        Start speed measuring.
        :param start_time: Start time if None it is now.
        """

        if start_time:
            self.start_time = start_time
        else:
            self.start_time = time.perf_counter()
        self.stop_time = None
        if self.events is None or self.seconds:
            self.events = 0
            self.seconds = 0.0

    def add_event(self):
        """ Add event. """

        if not self.start_time:
            raise RuntimeError('ProgressMeter is not started.')

        if self.events == self.total_events:
            raise RuntimeError('Number of events is larger than total events.')

        self.events += 1

    def add_events(self, events):
        """ Add events. """

        if not self.start_time:
            raise RuntimeError('ProgressMeter is not started.')

        if self.events + events > self.total_events:
            raise RuntimeError('Number of events is larger than total events.')

        if not isinstance(events, int):
            raise TypeError('events should integer.')

        if events <= 0:
            raise ValueError('events should be positive number.')

        self.events += events

    def subtract_total_event(self):
        """
        Remove/skip one total event to increase prediction accuracy.
        You can skip very fast operations (i.e. cached operations).
        It allows to focus on accurate measuring slow operations.
        """

        if not self.start_time:
            raise RuntimeError('ProgressMeter is not started.')

        if self.events == self.total_events:
            raise RuntimeError('Number of total events is smaller to events.')

        self.total_events -= 1

    def subtract_total_events(self, events):
        """
        Remove/skip some total events to increase prediction accuracy.
        You can skip very fast operations (i.e. cached operations).
        It allows to focus on accurate measuring slow operations.
        """

        if not self.start_time:
            raise RuntimeError('ProgressMeter is not started.')

        if self.events > self.total_events - events:
            raise RuntimeError('Number of total events is smaller to events.')

        if not isinstance(events, int):
            raise TypeError('events should integer.')

        if events <= 0:
            raise ValueError('events should be positive number.')

        self.total_events -= events

    def get_events(self):
        """
        Get total events counter since last reset.
        :return: Events counter or None if it has never started.
        """

        return self.events

    def get_seconds(self):
        """
        Get total seconds counter since last reset.
        :return: Seconds counter or None if it has never started.
        """

        # get total + current speed
        if self.start_time:
            now = time.perf_counter()
            seconds = now - self.start_time
            # add previous seconds
            seconds += self.seconds
            return seconds
        # get total speed
        else:
            return self.seconds

    def get_speed(self):
        """
        Get speed of events/seconds using now time or stop time since last reset.
        :return: speed or None if zero seconds
        """

        seconds = self.get_seconds()
        return self.events / seconds if seconds else None

    def get_progress(self):
        """
        Get progress.
        :return: Progress.
        """

        return self.events / float(self.total_events)

    def get_seconds_left(self):
        """
        Get seconds left to end.
        :return: Predicted seconds left to end or None.
        """

        speed = self.get_speed()
        if speed is None or speed == 0.0:
            return None

        events_left = self.total_events - self.events
        seconds_to_end = events_left / speed

        return seconds_to_end

    def get_statistics(self):
        """
        Get statistics.
        :return: Statistics string.
        """

        seconds_left = self.get_seconds_left()
        speed = self.get_speed()

        return 'done %s of %s %.2f%%, speed %s 1/s, operation %s s, time left %s' % (
            self.events,
            self.total_events,
            self.get_progress() * 100.0,
            '%e' % speed if speed else None,
            datetime.timedelta(seconds=1.0 / speed) if speed else None,
            datetime.timedelta(seconds=seconds_left) if seconds_left else None)

    def stop(self, stop_time=None):
        """
        Stop speed measuring.
        :param stop_time: Stop time if None it is now.
        """

        if self.start_time is None:
            raise RuntimeError('ProgressMeter is not started.')

        if stop_time:
            self.stop_time = stop_time
        else:
            self.stop_time = time.perf_counter()
        seconds = self.stop_time - self.start_time
        # add previous seconds
        self.seconds += seconds + self.seconds
        # reset times
        self.start_time = None
        self.stop_time = None

