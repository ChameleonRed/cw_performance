# coding=utf-8
__author__ = 'Cezary Wagner'
__copyright__ = 'Copyright 2015-2018, Cezary K. Wagner.'
__license__ = 'Apache License 2.0'
__version__ = '1.0'

import datetime


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

    SECONDS_PER_DAY = 24 * 60 * 60

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

        if start_time:
            self.start_time = start_time
        else:
            self.start_time = datetime.datetime.now()
        self.stop_time = None
        if self.events is None or self.seconds:
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

    @classmethod
    def _delta_to_seconds(cls, delta):
        seconds = delta.days * cls.SECONDS_PER_DAY + delta.seconds + delta.microseconds / 1e6
        return seconds

    def get_speed(self):
        """
        Get speed of events/seconds using now time or stop time since last reset.
        :return speed or None if zero seconds
        """

        # get total + current speed
        if self.start_time:
            now = datetime.datetime.now()
            delta = now - self.start_time
            seconds = self._delta_to_seconds(delta)
            # add previous seconds
            seconds += self.seconds
            return self.events / seconds if seconds else None
        # get total speed
        else:
            return self.events / self.seconds if self.seconds else None

    def get_events(self):
        """
        Get total events counter since last reset.
        :return Events counter or None if it has never started.
        """

        return self.events

    def get_seconds(self):
        """
        Get total seconds counter since last reset.
        :return Seconds counter or None if it has never started.
        """

        # get total + current speed
        if self.start_time:
            now = datetime.datetime.now()
            delta = now - self.start_time
            seconds = self._delta_to_seconds(delta)
            # add previous seconds
            seconds += self.seconds
            return seconds
        # get total speed
        else:
            return self.seconds

    def stop(self, stop_time=None):
        """
        Stop speed measuring.
        :param: stop_time: Stop time if None it is now.
        """

        if stop_time:
            self.stop_time = stop_time
        else:
            self.stop_time = datetime.datetime.now()
        delta = self.stop_time - self.start_time
        seconds = self._delta_to_seconds(delta)
        # add previous seconds
        self.seconds += seconds + self.seconds
        # reset times
        self.start_time = None
        self.stop_time = None

    def reset(self):
        """ Reset times, events and seconds counters. """

        self.start_time = None
        self.stop_time = None
        self.events = None
        self.seconds = None
