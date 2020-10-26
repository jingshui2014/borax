# coding=utf8

import unittest

from borax.counters.serials import generate_serials, SerialGenerator, StringSerialGenerator


class SerialGeneratorTestCase(unittest.TestCase):
    def test_func(self):
        source = [0, 1, 2, 4, 5, 7]
        res = generate_serials(upper=10, num=2, serials=source)
        self.assertListEqual([8, 9], res)
        res = generate_serials(upper=10, num=3, serials=source)
        self.assertListEqual([8, 9, 3], res)
        res = generate_serials(upper=10, num=4, serials=source)
        self.assertListEqual([8, 9, 3, 6], res)
        with self.assertRaises(ValueError):
            generate_serials(upper=10, num=5, serials=source)

    def test_serial_generator(self):
        sg = SerialGenerator(upper=10)
        res = sg.generate(3)
        self.assertListEqual([0, 1, 2], res)
        res = sg.generate(2)
        self.assertListEqual([3, 4], res)
        sg.remove([2, 3])
        res = sg.generate(4)
        self.assertListEqual([5, 6, 7, 8], res)
        res = sg.generate(3)
        self.assertListEqual([9, 2, 3], res)
        with self.assertRaises(ValueError):
            sg.generate(1)


class StringSerialGeneratorTestCase(unittest.TestCase):
    def test_string_serial(self):
        ssg = StringSerialGenerator(prefix='GCZ', digits=4)
        res = ssg.generate(2)
        self.assertListEqual(['GCZ0000', 'GCZ0001'], res)
        ssg.add(['GCZ0004'])
        res = ssg.generate(2)
        self.assertListEqual(['GCZ0005', 'GCZ0006'], res)

    def test_hex_serial(self):
        ssg = StringSerialGenerator(prefix='ff', digits=2, base=16)
        res = ssg.generate(2)
        self.assertListEqual(['ff00', 'ff01'], res)
        ssg.add(['ff0b'])
        res = ssg.generate(1)
        self.assertListEqual(['ff0c'], res)

    def test_error_base(self):
        with self.assertRaises(ValueError):
            StringSerialGenerator(prefix='CC', digits=2, base=3)

    def test_upper_edge_value(self):
        ssg = StringSerialGenerator(prefix='ff', digits=1, base=10)
        data = ssg.generate(num=10)
        self.assertEqual(10, len(data))
        self.assertEqual('ff9', data[-1])
