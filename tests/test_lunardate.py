# coding=utf8

import unittest

from datetime import date, timedelta

from borax.calendars.lunardate import LunarDate


class LunarDateTestCase(unittest.TestCase):
    def test_create_date(self):
        ld = LunarDate(1976, 8, 8, 1)
        self.assertEqual(1976, ld.year)
        self.assertEqual(8, ld.month)
        self.assertEqual(8, ld.day)
        self.assertEqual(True, ld.isLeapMonth)

    def test_convert_datetime(self):
        dt = LunarDate(1976, 8, 8, 1).toSolarDate()
        self.assertEqual(date(1976, 10, 1), dt)
        dt2 = LunarDate.fromSolarDate(2033, 10, 23)
        self.assertTrue(LunarDate(2033, 10, 1, 0), dt2)

        # day out of range
        with self.assertRaises(ValueError):
            LunarDate(2004, 1, 30).toSolarDate()

        # year out of range [1900, 2100]
        with self.assertRaises(ValueError):
            LunarDate(2101, 1, 1).toSolarDate()

    def test_timedelta(self):
        ld = LunarDate(1976, 8, 8)
        sd = date(2008, 1, 1)
        td = timedelta(days=10)

        self.assertEqual(timedelta(days=0), ld - ld)
        self.assertEqual(LunarDate(1976, 7, 27, 0), ld - td)
        self.assertEqual(timedelta(11444), sd - ld)
        self.assertEqual(LunarDate(1976, 8, 18, 0), ld + td)
        self.assertEqual(LunarDate(1976, 8, 18, 0), td + ld)

    def test_comparison(self):
        ld = LunarDate(1976, 8, 8)
        ld2 = LunarDate.today()
        self.assertTrue(ld < ld2)
        self.assertTrue(ld <= ld2)
        self.assertTrue(ld2 > ld)
        self.assertTrue(ld2 >= ld)
        self.assertTrue(ld != ld2)
        self.assertFalse(ld == ld2)
        self.assertTrue(LunarDate.today() == LunarDate.today())

        # Compare with a integer
        self.assertFalse(LunarDate.today() == 5)
        with self.assertRaises(TypeError):
            LunarDate.today() < 5
        with self.assertRaises(TypeError):
            LunarDate.today() > 5
        with self.assertRaises(TypeError):
            LunarDate.today() >= 5
        with self.assertRaises(TypeError):
            LunarDate.today() >= 5
