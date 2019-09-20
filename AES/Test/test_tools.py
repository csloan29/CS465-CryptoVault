# library imports
from unittest import TestCase
import numpy as np

# local file imports
from AES.ff_math import *


class TestTools(TestCase):

    def test_ff_add(self):
        # setup
        f1 = 0xd4
        f2 = 0xbe
        f_expected = 0x6a
        # test
        self.assertEqual(ff_add(f1, f2), f_expected)

    def test_x_time(self):
        # setup
        f1 = 0x57
        f2 = 0xae
        f1_expected = 0xae
        f2_expected = 0x47
        # test
        self.assertEqual(x_time(f1), f1_expected)
        self.assertEqual(x_time(f2), f2_expected)

    def test_ff_multiply(self):
        # setup
        f_start = 0x57
        f1 = 0x01  # right most bit only
        f2 = 0x80  # left most bit only
        f3 = 0x08  # leftmost bit with no bits to right
        f4 = 0x13  # leftmost bit with bits to right
        f1_expected = 0x57
        f2_expected = 0x38
        f3_expected = 0x8e
        f4_expected = 0xfe
        # tests
        self.assertEqual(ff_multiply(f_start, f1), f1_expected)
        self.assertEqual(ff_multiply(f_start, f2), f2_expected)
        self.assertEqual(ff_multiply(f_start, f3), f3_expected)
        self.assertEqual(ff_multiply(f_start, f4), f4_expected)