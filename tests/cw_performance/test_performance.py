# coding=utf-8
__author__ = 'Cezary Wagner'
__copyright__ = 'Copyright 2015-2019, Cezary K. Wagner.'
__license__ = 'Apache License 2.0'
__version__ = '1.0'

import unittest

import time

from cw_performance.performance import Speedometer, ProgressMeter


class TestSpeedometer(unittest.TestCase):
    def test_basic_flow(self):
        s = Speedometer()
        # first start
        s.start()
        s.get_speed()
        time.sleep(0.01)
        s.add_event()
        s.add_events(2)
        s.get_speed()

        # first stop
        s.stop()
        s.get_speed()
        s.get_events()
        s.get_seconds()

        # second start
        s.start()
        s.get_speed()
        time.sleep(0.01)
        s.add_event()
        s.add_events(2)
        s.get_speed()

        # second stop
        s.stop()
        s.get_speed()
        s.get_events()
        s.get_seconds()

    def test_is_not_started_add_event(self):
        s = Speedometer()
        with self.assertRaises(RuntimeError):
            s.add_event()

        with self.assertRaises(RuntimeError):
            s.add_events(2)

    def test_is_not_started_stop(self):
        s = Speedometer()
        with self.assertRaises(RuntimeError):
            s.stop()

    def test_is_already_stopped(self):
        s = Speedometer()
        s.start()
        s.stop()
        with self.assertRaises(RuntimeError):
            s.stop()

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


class TestProgressMeter(unittest.TestCase):
    def test_basic_flow(self):
        s = ProgressMeter(total_events=100)

        # first start
        s.start()
        s.subtract_total_event()
        s.get_progress()
        s.get_seconds_left()
        s.get_statistics()
        s.get_speed()
        time.sleep(0.01)
        s.add_event()
        s.add_events(2)
        s.get_speed()

        # first stop
        s.stop()
        s.get_progress()
        s.get_seconds_left()
        s.get_statistics()
        s.get_speed()
        s.get_events()
        s.get_seconds()

        # second start
        s.start()
        s.subtract_total_event()
        s.get_progress()
        s.get_seconds_left()
        s.get_statistics()
        s.get_speed()
        time.sleep(0.01)
        s.add_event()
        s.add_events(2)
        s.get_speed()

        # second stop
        s.stop()
        s.get_progress()
        s.get_seconds_left()
        s.get_speed()
        s.get_events()
        s.get_seconds()

    def test_is_not_started_add_event(self):
        s = ProgressMeter(total_events=100)
        with self.assertRaises(RuntimeError):
            s.add_event()

        with self.assertRaises(RuntimeError):
            s.add_events(2)

        s.start()
        s.stop()
        with self.assertRaises(RuntimeError):
            s.add_event()

        with self.assertRaises(RuntimeError):
            s.add_events(2)

    def test_is_not_started_stop(self):
        s = ProgressMeter(total_events=100)
        with self.assertRaises(RuntimeError):
            s.stop()

    def test_is_already_stopped(self):
        s = Speedometer()
        s.start()
        s.stop()
        with self.assertRaises(RuntimeError):
            s.stop()

    def test_events_counter(self):
        s = ProgressMeter(total_events=100)
        self.assertEqual(s.get_events(), None)
        s.start()
        self.assertEqual(s.get_events(), 0)
        s.add_event()
        self.assertEqual(s.get_events(), 1)
        s.add_events(2)
        self.assertEqual(s.get_events(), 3)
        s.stop()
        self.assertEqual(s.get_events(), 3)

