# coding=utf-8
__author__ = 'Cezary Wagner'
__copyright__ = 'Copyright 2015-2018, Cezary K. Wagner.'
__license__ = 'Apache License 2.0'
__version__ = '1.0'

import unittest

import time

from cw_performance.performance import Speedometer


class TestSpeedometer(unittest.TestCase):
    def test_basic_flow(self):
        s = Speedometer()
        s.start()
        s.add_event()
        s.add_events(2)
        s.stop()
        s.get_speed()
        s.get_events()
        s.get_seconds()

        s.reset()
        s.start()
        s.add_event()
        s.add_events(2)
        s.stop()
        s.get_speed()
        s.get_events()
        s.get_seconds()

    def test_is_not_started(self):
        s = Speedometer()
        with self.assertRaises(RuntimeError):
            s.add_event()

        with self.assertRaises(RuntimeError):
            s.add_events(2)

    def test_events_counter(self):
        s = Speedometer()
        self.assertEqual(s.get_events(), None)
        s.start()
        self.assertEqual(s.get_events(), 0)
        s.add_event()
        self.assertEqual(s.get_events(), 1)
        s.add_events(2)
        self.assertEqual(s.get_events(), 3)
        s.stop()
        self.assertEqual(s.get_events(), 3)

    def test_seconds_counter(self):
        s = Speedometer()
        self.assertEqual(s.get_seconds(), None)
        s.start()
        time.sleep(0.01)
        self.assertGreaterEqual(s.get_seconds(), 0.01)
        s.stop()
        t = s.get_seconds()
        self.assertGreaterEqual(s.get_seconds(), 0.01)
        self.assertEqual(s.get_seconds(), t)

